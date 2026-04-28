"""
Generate acid-base titration curve scaffolds.

Run from article directory:
    python python/03_titration_curves.py
"""

from pathlib import Path
import pandas as pd

from acid_base_core import titration_curves


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "titration_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "titration_curves.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = titration_curves(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.head(20).round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
