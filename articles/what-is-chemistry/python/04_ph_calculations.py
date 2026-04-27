"""
Calculate simplified pH values.

Run from article directory:
    python python/04_ph_calculations.py
"""

from pathlib import Path
import pandas as pd

from chemistry_intro_core import calculate_ph


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "ph_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "ph_calculations.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    result = calculate_ph(examples)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(4).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
