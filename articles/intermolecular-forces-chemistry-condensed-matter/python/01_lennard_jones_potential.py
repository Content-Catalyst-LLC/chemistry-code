"""
Calculate Lennard-Jones potential curves for simplified pair interactions.

Run from article directory:
    python python/01_lennard_jones_potential.py
"""

from pathlib import Path
import pandas as pd

from condensed_matter_core import lennard_jones_table, lennard_jones_minima


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "pair_potential_parameters.csv"
POTENTIAL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "lennard_jones_potentials.csv"
MINIMA_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "lennard_jones_minima.csv"


def main() -> None:
    POTENTIAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    parameters = pd.read_csv(INPUT_PATH)
    potentials = lennard_jones_table(parameters)
    minima = lennard_jones_minima(potentials)

    potentials.to_csv(POTENTIAL_OUTPUT, index=False)
    minima.to_csv(MINIMA_OUTPUT, index=False)

    print("Lennard-Jones minima")
    print(minima.round(6).to_string(index=False))
    print(f"Saved: {POTENTIAL_OUTPUT}")


if __name__ == "__main__":
    main()
