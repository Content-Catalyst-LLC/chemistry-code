"""
Standardize assay units and calculate pIC50-like activity values.

Run from article directory:
    python python/03_assay_standardization.py
"""

from pathlib import Path
import pandas as pd

from cheminformatics_core import assay_standardization


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "assays.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "assay_standardization.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = assay_standardization(pd.read_csv(INPUT_PATH))
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
