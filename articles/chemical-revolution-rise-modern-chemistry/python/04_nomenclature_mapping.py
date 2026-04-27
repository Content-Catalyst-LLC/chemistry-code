"""
Organize simplified historical-to-modern nomenclature mappings.

Run from article directory:
    python python/04_nomenclature_mapping.py
"""

from pathlib import Path
import pandas as pd

from chemical_revolution_core import organize_nomenclature


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "nomenclature_mapping.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "nomenclature_mapping.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    mapping = pd.read_csv(INPUT_PATH)
    result = organize_nomenclature(mapping)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
