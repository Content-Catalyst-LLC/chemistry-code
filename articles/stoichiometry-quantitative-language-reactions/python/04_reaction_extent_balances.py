"""
Calculate final amounts from reaction extent.

Run from article directory:
    python python/04_reaction_extent_balances.py
"""

from pathlib import Path
import pandas as pd

from stoichiometry_core import reaction_extent_balances


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "reaction_extent_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "reaction_extent_balances.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = reaction_extent_balances(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
