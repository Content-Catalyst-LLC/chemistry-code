"""
Check conservation of mass in simplified examples.

Run from article directory:
    python python/01_mass_conservation.py
"""

from pathlib import Path
import pandas as pd

from chemical_revolution_core import check_mass_conservation


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "mass_conservation_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "mass_conservation.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    result = check_mass_conservation(examples)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
