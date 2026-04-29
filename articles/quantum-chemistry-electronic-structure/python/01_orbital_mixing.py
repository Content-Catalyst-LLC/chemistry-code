"""
Calculate two-level orbital mixing examples.

Run from article directory:
    python python/01_orbital_mixing.py
"""

from pathlib import Path
import pandas as pd

from quantum_chemistry_core import orbital_mixing


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "orbital_mixing_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "orbital_mixing.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = orbital_mixing(pd.read_csv(INPUT_PATH))
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
