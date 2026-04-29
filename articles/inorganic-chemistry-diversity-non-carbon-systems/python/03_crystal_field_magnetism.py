"""
Calculate simplified crystal-field and magnetic descriptors.

Run from article directory:
    python python/03_crystal_field_magnetism.py
"""

from pathlib import Path
import pandas as pd

from inorganic_core import crystal_field_magnetism


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "crystal_field_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "crystal_field_magnetism.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = crystal_field_magnetism(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
