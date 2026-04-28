"""
Summarize periodic-table sample features.

Run from article directory:
    python python/01_element_features.py
"""

from pathlib import Path
import pandas as pd

from periodic_core import summarize_element_features


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "elements_sample.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "element_features_summary.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    elements = pd.read_csv(INPUT_PATH)
    summary = summarize_element_features(elements)
    summary.to_csv(OUTPUT_PATH, index=False)

    print("Element feature summary")
    print(summary.to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
