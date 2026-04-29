"""
Calculate Arrhenius temperature dependence.

Run from article directory:
    python python/02_arrhenius_kinetics.py
"""

from pathlib import Path
import pandas as pd

from physical_chemistry_core import arrhenius_kinetics


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "arrhenius_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "arrhenius_kinetics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = arrhenius_kinetics(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
