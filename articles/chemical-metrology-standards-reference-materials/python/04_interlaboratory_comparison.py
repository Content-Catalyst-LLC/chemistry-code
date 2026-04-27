"""
Calculate normalized error for interlaboratory comparison.

Run from article directory:
    python python/04_interlaboratory_comparison.py
"""

from pathlib import Path
import pandas as pd

from metrology_core import calculate_interlaboratory_en


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "interlaboratory_comparison.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "interlaboratory_comparison.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    comparison = pd.read_csv(INPUT_PATH)
    result = calculate_interlaboratory_en(comparison)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(4).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
