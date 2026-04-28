"""
Analyze simplified periodic trends.

Run from article directory:
    python python/03_periodic_trends.py
"""

from pathlib import Path
import pandas as pd

from periodic_core import calculate_periodic_trends


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "elements_sample.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "periodic_trends.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    elements = pd.read_csv(INPUT_PATH)
    trends = calculate_periodic_trends(elements)
    trends.to_csv(OUTPUT_PATH, index=False)

    print("Periodic trend models")
    print(trends.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
