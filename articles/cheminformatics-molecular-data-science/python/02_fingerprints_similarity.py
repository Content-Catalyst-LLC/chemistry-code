"""
Calculate pairwise Tanimoto similarity for molecular fingerprints.

Run from article directory:
    python python/02_fingerprints_similarity.py
"""

from pathlib import Path
import pandas as pd

from cheminformatics_core import pairwise_tanimoto


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "fingerprints.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "fingerprints_similarity.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = pairwise_tanimoto(pd.read_csv(INPUT_PATH))
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
