"""
Calculate Gibbs free energy, equilibrium constants, and nonstandard free energy.

Run from article directory:
    python python/03_gibbs_equilibrium.py
"""

from pathlib import Path
import pandas as pd

from thermodynamics_core import gibbs_equilibrium


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "gibbs_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "gibbs_equilibrium.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = gibbs_equilibrium(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
