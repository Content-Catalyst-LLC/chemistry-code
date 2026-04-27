"""
Calculate a chemical measurement uncertainty budget.

Run from article directory:
    python python/01_uncertainty_budget.py
"""

from pathlib import Path
import pandas as pd

from metrology_core import summarize_uncertainty_budget


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "uncertainty_budget.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "uncertainty_budget_summary.csv"
CONTRIBUTION_PATH = ARTICLE_DIR / "outputs" / "tables" / "uncertainty_budget_contributions.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    budget = pd.read_csv(INPUT_PATH)
    contributions, summary = summarize_uncertainty_budget(budget, coverage_factor=2.0)

    summary.to_csv(OUTPUT_PATH, index=False)
    contributions.to_csv(CONTRIBUTION_PATH, index=False)

    print(summary.round(6).to_string(index=False))
    print(contributions.round(4).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Saved: {CONTRIBUTION_PATH}")


if __name__ == "__main__":
    main()
