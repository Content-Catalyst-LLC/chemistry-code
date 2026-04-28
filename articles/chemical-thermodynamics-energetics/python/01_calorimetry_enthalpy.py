"""
Calculate calorimetry heat transfer and reaction enthalpy.

Run from article directory:
    python python/01_calorimetry_enthalpy.py
"""

from pathlib import Path
import pandas as pd

from thermodynamics_core import calorimetry_enthalpy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "calorimetry_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "calorimetry_enthalpy.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = calorimetry_enthalpy(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
