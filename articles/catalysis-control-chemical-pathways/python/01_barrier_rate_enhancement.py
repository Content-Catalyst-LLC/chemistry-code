"""
Estimate catalytic rate enhancement from barrier lowering.

Run from article directory:
    python python/01_barrier_rate_enhancement.py
"""

from pathlib import Path
import pandas as pd

from catalysis_core import barrier_rate_enhancement


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "barrier_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "barrier_rate_enhancement.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = barrier_rate_enhancement(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
