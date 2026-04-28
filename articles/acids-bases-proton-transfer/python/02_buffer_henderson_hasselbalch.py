"""
Calculate buffer pH using Henderson-Hasselbalch relationship.

Run from article directory:
    python python/02_buffer_henderson_hasselbalch.py
"""

from pathlib import Path
import pandas as pd

from acid_base_core import buffer_ph


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "buffer_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "buffer_henderson_hasselbalch.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = buffer_ph(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
