"""
Summarize periodic classification by block, category, family, and period.

Run from article directory:
    python python/01_periodic_classification.py
"""

from pathlib import Path
import pandas as pd

from periodic_classification_core import summarize_classification


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "elements_classification.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "periodic_classification_summary.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    elements = pd.read_csv(INPUT_PATH)
    summaries = summarize_classification(elements)

    combined = pd.concat(
        [
            table.assign(summary_type=name).astype(str)
            for name, table in summaries.items()
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(OUTPUT_PATH, index=False)

    for name, table in summaries.items():
        print(f"\n{name}")
        print(table.to_string(index=False))

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
