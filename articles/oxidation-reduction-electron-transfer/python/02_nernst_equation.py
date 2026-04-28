"""
Calculate Nernst potentials under nonstandard conditions.

Run from article directory:
    python python/02_nernst_equation.py
"""

from pathlib import Path
import pandas as pd

from redox_core import nernst_equation


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "nernst_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "nernst_equation.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = nernst_equation(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
