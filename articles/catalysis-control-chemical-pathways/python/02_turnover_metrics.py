"""
Calculate turnover number, turnover frequency, and catalytic activity.

Run from article directory:
    python python/02_turnover_metrics.py
"""

from pathlib import Path
import pandas as pd

from catalysis_core import turnover_metrics


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "turnover_experiments.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "turnover_metrics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = turnover_metrics(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(8).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
