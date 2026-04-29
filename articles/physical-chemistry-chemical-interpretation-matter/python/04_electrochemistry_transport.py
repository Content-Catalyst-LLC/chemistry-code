"""
Calculate electrochemical free energy and Nernst potentials.

Run from article directory:
    python python/04_electrochemistry_transport.py
"""

from pathlib import Path
import pandas as pd

from physical_chemistry_core import electrochemistry_table


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "electrochemistry_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "electrochemistry_transport.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = electrochemistry_table(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
