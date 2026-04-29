"""
Calculate thermodynamic and equilibrium descriptors.

Run from article directory:
    python python/01_thermodynamics_equilibrium.py
"""

from pathlib import Path
import pandas as pd

from physical_chemistry_core import thermodynamics_equilibrium


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "thermodynamic_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "thermodynamics_equilibrium.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = thermodynamics_equilibrium(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
