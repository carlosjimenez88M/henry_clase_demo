"""
Currency Price Tool for AI Agent.

This tool fetches real-time currency exchange rates using a free API.
Includes caching to reduce API calls and fallback to mock data for reliability.
"""

import re
from datetime import datetime, timedelta

import requests
from langchain.tools import BaseTool
from pydantic import Field


class CurrencyPriceTool(BaseTool):
    """Tool for fetching real-time currency exchange rates."""

    name: str = "currency_price_checker"
    description: str = """
    Real-time currency exchange rates. Use this tool to get current prices for currency pairs.
    Supports: USD, EUR, GBP, JPY, CHF, CAD, AUD, MXN, BRL, CNY

    Input should specify the currencies, like:
    - "USD to EUR"
    - "euro dollar rate"
    - "current EUR price"
    - "100 USD in GBP"

    Output includes exchange rate, timestamp, and conversion example.
    """

    # Internal state
    cache: dict[str, tuple[dict, datetime]] = Field(default_factory=dict, exclude=True)
    cache_ttl: int = Field(default=300, exclude=True)  # 5 minutes
    supported_currencies: list = Field(
        default=["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "MXN", "BRL", "CNY"],
        exclude=True,
    )
    api_url: str = Field(
        default="https://api.exchangerate-api.com/v4/latest/", exclude=True
    )

    def _run(self, query: str) -> str:
        """
        Fetch currency exchange rate.

        Args:
            query: Natural language query for currency exchange

        Returns:
            Formatted string with exchange rate information
        """
        # Parse currency pair from query
        from_currency, to_currency, amount = self._parse_query(query)

        if not from_currency or not to_currency:
            return self._format_error(
                "Could not understand currency query. "
                "Please specify currencies like 'USD to EUR' or 'dollar to euro'."
            )

        # Get exchange rate
        try:
            rate = self._get_exchange_rate(from_currency, to_currency)
            if rate is None:
                return self._use_fallback_data(from_currency, to_currency, amount)

            return self._format_result(from_currency, to_currency, rate, amount)

        except Exception:
            return self._use_fallback_data(from_currency, to_currency, amount)

    def _parse_query(self, query: str) -> tuple[str | None, str | None, float]:
        """
        Parse currency query to extract from/to currencies and amount.

        Returns:
            Tuple of (from_currency, to_currency, amount)
        """
        query_upper = query.upper()
        amount = 1.0  # Default amount

        # Extract amount if present
        amount_match = re.search(r"(\d+(?:\.\d+)?)", query)
        if amount_match:
            amount = float(amount_match.group(1))

        # Currency name mappings
        currency_names = {
            "DOLLAR": "USD",
            "DOLAR": "USD",
            "EURO": "EUR",
            "POUND": "GBP",
            "STERLING": "GBP",
            "YEN": "JPY",
            "FRANC": "CHF",
            "CANADIAN": "CAD",
            "AUSTRALIAN": "AUD",
            "AUSSIE": "AUD",
            "PESO": "MXN",
            "REAL": "BRL",
            "YUAN": "CNY",
            "RENMINBI": "CNY",
        }

        # Replace currency names with codes
        for name, code in currency_names.items():
            query_upper = query_upper.replace(name, code)

        # Find currency codes in query
        found_currencies = []
        for curr in self.supported_currencies:
            if curr in query_upper:
                found_currencies.append(curr)

        # Determine from/to based on context
        if len(found_currencies) >= 2:
            return found_currencies[0], found_currencies[1], amount
        elif len(found_currencies) == 1:
            # Default to USD if only one currency specified
            if found_currencies[0] == "USD":
                return "USD", "EUR", amount  # Default to EUR
            else:
                return "USD", found_currencies[0], amount

        return None, None, amount

    def _get_exchange_rate(
        self, from_currency: str, to_currency: str
    ) -> float | None:
        """
        Get exchange rate from API or cache.

        Args:
            from_currency: Source currency code
            to_currency: Target currency code

        Returns:
            Exchange rate or None if failed
        """
        cache_key = f"{from_currency}_{to_currency}"

        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=self.cache_ttl):
                return cached_data.get(to_currency)

        # Fetch from API
        try:
            url = f"{self.api_url}{from_currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            rates = data.get("rates", {})

            # Cache the result
            self.cache[cache_key] = (rates, datetime.now())

            return rates.get(to_currency)

        except Exception as e:
            print(f"API error: {e}")
            return None

    def _use_fallback_data(
        self, from_currency: str, to_currency: str, amount: float
    ) -> str:
        """Use mock/fallback data when API fails."""
        # Mock exchange rates (approximate values for demo)
        mock_rates = {
            ("USD", "EUR"): 0.92,
            ("USD", "GBP"): 0.79,
            ("USD", "JPY"): 149.50,
            ("USD", "CHF"): 0.88,
            ("USD", "CAD"): 1.35,
            ("USD", "AUD"): 1.52,
            ("USD", "MXN"): 17.20,
            ("USD", "BRL"): 4.98,
            ("USD", "CNY"): 7.24,
            ("EUR", "USD"): 1.09,
            ("GBP", "USD"): 1.27,
        }

        rate = mock_rates.get((from_currency, to_currency))

        if rate is None:
            # Try inverse
            inverse_rate = mock_rates.get((to_currency, from_currency))
            if inverse_rate:
                rate = 1 / inverse_rate

        if rate is None:
            return self._format_error(
                f"Unable to fetch exchange rate for {from_currency} to {to_currency}. "
                "API unavailable and no mock data for this pair."
            )

        result = self._format_result(from_currency, to_currency, rate, amount)
        result += "\n\n  Note: Using cached/mock data (API temporarily unavailable)"
        return result

    def _format_result(
        self, from_currency: str, to_currency: str, rate: float, amount: float
    ) -> str:
        """Format the exchange rate result."""
        converted_amount = amount * rate
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        result = (
            f"Current exchange rate: 1 {from_currency} = {rate:.4f} {to_currency}\n"
        )
        result += f"(as of {timestamp})\n\n"
        result += "This means:\n"
        result += (
            f"  {amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}\n"
        )

        # Add additional context
        if amount == 1:
            result += f"  100 {from_currency} = {(rate * 100):.2f} {to_currency}\n"

        return result

    def _format_error(self, message: str) -> str:
        """Format error message."""
        return (
            f"Error: {message}\n\n"
            "Supported currencies: USD, EUR, GBP, JPY, CHF, CAD, AUD, MXN, BRL, CNY\n"
            "Example queries:\n"
            "  - 'USD to EUR'\n"
            "  - '100 dollars in euros'\n"
            "  - 'current pound sterling rate'"
        )

    async def _arun(self, query: str) -> str:
        """Async version (not implemented, falls back to sync)."""
        return self._run(query)
