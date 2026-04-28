"""
Calculate standard cell potentials, Gibbs free energy, and equilibrium constants.

Run from article directory:
    python python/01_cell_potential_gibbs.py
"""

from pathlib import Path
import pandas as pd

from redox_core import cell_potential_gibbs


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "cell_potential_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "cell_potential_gibbs.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = cell_potential_gibbs(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
