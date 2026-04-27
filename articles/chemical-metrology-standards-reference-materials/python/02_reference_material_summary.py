"""
Summarize synthetic reference material records.

Run from article directory:
    python python/02_reference_material_summary.py
"""

from pathlib import Path
import pandas as pd

from metrology_core import summarize_reference_materials


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "reference_materials.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "reference_material_summary.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    materials = pd.read_csv(INPUT_PATH)
    result = summarize_reference_materials(materials)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(4).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
