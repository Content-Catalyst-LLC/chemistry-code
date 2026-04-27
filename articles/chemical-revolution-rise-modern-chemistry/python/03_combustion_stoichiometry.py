"""
Calculate simplified carbon combustion stoichiometry.

Run from article directory:
    python python/03_combustion_stoichiometry.py
"""

from pathlib import Path
import pandas as pd

from chemical_revolution_core import calculate_combustion_stoichiometry


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "combustion_stoichiometry.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "combustion_stoichiometry.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    result = calculate_combustion_stoichiometry(examples)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
