"""
Calculate Boltzmann populations for conformer energies.

Run from article directory:
    python python/02_conformer_boltzmann.py
"""

from pathlib import Path
import pandas as pd

from computational_chemistry_core import conformer_boltzmann


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "conformer_energies.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "conformer_boltzmann.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = conformer_boltzmann(pd.read_csv(INPUT_PATH))
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
