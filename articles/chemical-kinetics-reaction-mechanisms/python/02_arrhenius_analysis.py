"""
Estimate activation energy from Arrhenius data.

Run from article directory:
    python python/02_arrhenius_analysis.py
"""

from pathlib import Path
import pandas as pd

from kinetics_core import arrhenius_analysis


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "arrhenius_data.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "arrhenius_analysis.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = arrhenius_analysis(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
