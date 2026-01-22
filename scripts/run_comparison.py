"""
Script to run model comparison.

Usage:
    python scripts/run_comparison.py [--models MODEL1,MODEL2,MODEL3] [--output PATH]

Examples:
    python scripts/run_comparison.py
    python scripts/run_comparison.py --models gpt-4o-mini,gpt-4o
    python scripts/run_comparison.py --output results/comparison.json
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.comparison.evaluator import ModelEvaluator


def main():
    """Main function to run model comparison."""
    parser = argparse.ArgumentParser(description="Run model comparison evaluation")
    parser.add_argument(
        "--models",
        type=str,
        default="gpt-4o-mini,gpt-4o,gpt-5-nano",
        help="Comma-separated list of models to compare"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/comparison_results.json",
        help="Output path for results"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    # Parse models
    models = [m.strip() for m in args.models.split(",")]

    print(" Pink Floyd AI Agent - Model Comparison")
    print("="*70)
    print(f"Models to test: {', '.join(models)}")
    print(f"Output: {args.output}")
    print("="*70 + "\n")

    # Create evaluator
    evaluator = ModelEvaluator(models)

    # Run evaluation
    evaluator.run_evaluation(verbose=not args.quiet)

    # Print summary
    evaluator.print_summary()

    # Save results
    output_path = Path(args.output)
    evaluator.save_results(output_path)

    print("\n Comparison complete!")


if __name__ == "__main__":
    main()
