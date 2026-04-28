"""
Compute simplified element similarity distances.

Run from article directory:
    python python/03_element_similarity.py
"""

from pathlib import Path
import pandas as pd

from periodic_classification_core import compute_element_similarity


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "elements_classification.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "element_similarity.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    elements = pd.read_csv(INPUT_PATH)
    similarity = compute_element_similarity(elements)
    similarity.to_csv(OUTPUT_PATH, index=False)

    print(similarity.head(20).round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
