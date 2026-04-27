"""
Summarize a synthetic traceability chain.

Run from article directory:
    python python/03_traceability_chain.py
"""

from pathlib import Path
import pandas as pd

from metrology_core import summarize_traceability_chain


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "traceability_chain.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "traceability_chain_summary.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    chain = pd.read_csv(INPUT_PATH)
    result = summarize_traceability_chain(chain)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
