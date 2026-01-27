"""
LangGraph Dev Server Entry Points.

This module provides parameterless functions that return compiled graphs
for use with the LangGraph dev server.
"""

from langchain_core.tools import tool

from src.agents.langgraph_react_agent import create_langgraph_react_agent
from src.tools.currency_tool import CurrencyPriceTool
from src.tools.database_tool import PinkFloydDatabaseTool


def pink_floyd_react_agent():
    """
    Create and return a compiled LangGraph for Pink Floyd ReAct agent.

    This agent has access to:
    - Pink Floyd database tool
    - Currency exchange rate tool

    Returns:
        Compiled LangGraph StateGraph
    """
    # Initialize tools
    tools = [
        PinkFloydDatabaseTool(),
        CurrencyPriceTool()
    ]

    # Create and return compiled graph
    return create_langgraph_react_agent(
        model_name="gpt-4o-mini",
        tools=tools,
        temperature=0.1
    )


def cinema_react_agent():
    """
    Create and return a compiled LangGraph for Cinema ReAct agent.

    This agent has access to cinema analysis tools for movie information.

    Returns:
        Compiled LangGraph StateGraph
    """
    # Define cinema database (same as in notebook)
    CINEMA_DATABASE = [
        {
            "id": 1,
            "title": "2001: A Space Odyssey",
            "director": "Stanley Kubrick",
            "year": 1968,
            "genres": ["Ciencia Ficción", "Drama"],
            "themes": ["Evolución humana", "Inteligencia artificial", "Existencialismo"],
            "symbolism": "El monolito representa el conocimiento y la evolución.",
            "rating": 8.3
        },
        {
            "id": 2,
            "title": "The Shining",
            "director": "Stanley Kubrick",
            "year": 1980,
            "genres": ["Terror", "Psicológico"],
            "themes": ["Aislamiento", "Locura", "Violencia doméstica"],
            "symbolism": "El hotel representa el pasado oscuro.",
            "rating": 8.4
        },
        {
            "id": 3,
            "title": "Inception",
            "director": "Christopher Nolan",
            "year": 2010,
            "genres": ["Ciencia Ficción", "Thriller"],
            "themes": ["Realidad vs sueños", "Culpa y pérdida", "Subconsciencia"],
            "symbolism": "El tótem representa la búsqueda de verdad.",
            "rating": 8.8
        },
        {
            "id": 4,
            "title": "The Dark Knight",
            "director": "Christopher Nolan",
            "year": 2008,
            "genres": ["Acción", "Crimen", "Drama"],
            "themes": ["Caos vs orden", "Dualidad", "Heroísmo"],
            "symbolism": "El Joker representa el caos anarquista.",
            "rating": 9.0
        },
        {
            "id": 5,
            "title": "Pulp Fiction",
            "director": "Quentin Tarantino",
            "year": 1994,
            "genres": ["Crimen", "Drama"],
            "themes": ["Redención", "Violencia", "Destino vs libre albedrío"],
            "symbolism": "El maletín representa lo inalcanzable.",
            "rating": 8.9
        }
    ]

    @tool
    def cinema_database_search(query: str) -> str:
        """Busca películas por director, género, tema o título en la base de datos de cine."""
        query_lower = query.lower()
        results = []

        for movie in CINEMA_DATABASE:
            match = False

            if movie['director'].lower() in query_lower:
                match = True
            if any(genre.lower() in query_lower for genre in movie['genres']):
                match = True
            if any(theme.lower() in query_lower for theme in movie['themes']):
                match = True
            if movie['title'].lower() in query_lower:
                match = True

            if match:
                results.append(movie)

        if not results:
            return "No se encontraron películas."

        output = f"Se encontraron {len(results)} película(s):\n\n"
        for movie in results:
            output += f"{movie['title']} ({movie['year']})\n"
            output += f"  Director: {movie['director']}\n"
            output += f"  Géneros: {', '.join(movie['genres'])}\n"
            output += f"  Rating: {movie['rating']}/10\n\n"

        return output

    @tool
    def thematic_analysis(movie_title: str) -> str:
        """Análisis profundo de temas y simbolismo de una película específica."""
        movie = None
        for m in CINEMA_DATABASE:
            if movie_title.lower() in m['title'].lower():
                movie = m
                break

        if not movie:
            return f"No se encontró la película '{movie_title}'."

        analysis = f"ANÁLISIS: {movie['title']} ({movie['year']})\n"
        analysis += f"Director: {movie['director']}\n\n"
        analysis += f"TEMAS:\n"
        for i, theme in enumerate(movie['themes'], 1):
            analysis += f"  {i}. {theme}\n"
        analysis += f"\nSIMBOLISMO: {movie['symbolism']}\n"

        return analysis

    @tool
    def director_style_comparison(director_name: str) -> str:
        """Analiza el estilo de un director comparando sus películas."""
        director_movies = [m for m in CINEMA_DATABASE if director_name.lower() in m['director'].lower()]

        if not director_movies:
            return f"No se encontraron películas del director '{director_name}'."

        analysis = f"ANÁLISIS: {director_movies[0]['director']}\n"
        analysis += f"Películas: {len(director_movies)}\n\n"

        for movie in sorted(director_movies, key=lambda x: x['year']):
            analysis += f"  {movie['title']} ({movie['year']}) - {movie['rating']}/10\n"

        avg_rating = sum(m['rating'] for m in director_movies) / len(director_movies)
        analysis += f"\nRating promedio: {avg_rating:.2f}/10\n"

        return analysis

    # Create cinema tools list
    cinema_tools = [
        cinema_database_search,
        thematic_analysis,
        director_style_comparison
    ]

    # Create and return compiled graph
    return create_langgraph_react_agent(
        model_name="gpt-4o-mini",
        tools=cinema_tools,
        temperature=0.1
    )
