"""
Calculate replicate precision and expanded uncertainty.

Run from article directory:
    python python/03_replicate_uncertainty.py
"""

from pathlib import Path
import pandas as pd

from measurement_quantification_core import summarize_replicates


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "replicate_measurements.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "replicate_uncertainty.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = summarize_replicates(data, coverage_factor=2.0)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(8).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
