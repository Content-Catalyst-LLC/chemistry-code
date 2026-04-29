"""
Calculate Michaelis-Menten enzyme kinetics.

Run from article directory:
    python python/01_enzyme_kinetics.py
"""

from pathlib import Path
import pandas as pd

from biochemistry_core import michaelis_menten


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "enzyme_kinetics_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "enzyme_kinetics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = michaelis_menten(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
