"""
Calculate electronegativity differences and simplified bond polarity classes.

Run from article directory:
    python python/02_bond_polarity.py
"""

from pathlib import Path
import pandas as pd

from bonding_core import calculate_bond_polarity


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "bond_polarity_sample.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "bond_polarity.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    bonds = pd.read_csv(INPUT_PATH)
    result = calculate_bond_polarity(bonds)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(4).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
