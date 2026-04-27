"""
Calculate mass gain in simplified oxidation examples.

Run from article directory:
    python python/02_oxidation_mass_gain.py
"""

from pathlib import Path
import pandas as pd

from chemical_revolution_core import calculate_oxidation_mass_gain


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "oxidation_mass_gain.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "oxidation_mass_gain.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    result = calculate_oxidation_mass_gain(examples)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
