"""
Calculate amount of substance and molarity.

Run from article directory:
    python python/01_moles_molarity_dilution.py
"""

from pathlib import Path
import pandas as pd

from chemistry_intro_core import add_moles_and_molarity


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "intro_chemistry_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "moles_molarity_dilution.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    result = add_moles_and_molarity(examples)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
