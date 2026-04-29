"""
Calculate Lennard-Jones and Coulomb potential scaffolds.

Run from article directory:
    python python/02_potentials.py
"""

from pathlib import Path
import pandas as pd

from molecular_dynamics_core import lennard_jones, coulomb_energy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
LJ_INPUT = ARTICLE_DIR / "data" / "lennard_jones_cases.csv"
COULOMB_INPUT = ARTICLE_DIR / "data" / "coulomb_cases.csv"

LJ_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "lennard_jones.csv"
COULOMB_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "coulomb_energy.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "potentials.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    lj = lennard_jones(pd.read_csv(LJ_INPUT))
    coulomb = coulomb_energy(pd.read_csv(COULOMB_INPUT))

    lj.to_csv(LJ_OUTPUT, index=False)
    coulomb.to_csv(COULOMB_OUTPUT, index=False)

    combined = pd.concat(
        [
            lj.astype(str).assign(table_type="lennard_jones"),
            coulomb.astype(str).assign(table_type="coulomb_energy"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Lennard-Jones")
    print(lj.round(6).to_string(index=False))
    print("\nCoulomb")
    print(coulomb.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
