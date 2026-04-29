"""
Calculate simple spectral matching scores and report-ready summary.

Run from article directory:
    python python/04_spectral_matching_reporting.py
"""

from pathlib import Path
import pandas as pd

from analytical_core import spectral_similarity


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "spectral_vectors.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "spectral_matching_reporting.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = spectral_similarity(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(8).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
