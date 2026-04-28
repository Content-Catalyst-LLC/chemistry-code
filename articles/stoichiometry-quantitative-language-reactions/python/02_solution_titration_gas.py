"""
Calculate solution preparation, titration equivalence, and gas stoichiometry.

Run from article directory:
    python python/02_solution_titration_gas.py
"""

from pathlib import Path
import pandas as pd

from stoichiometry_core import dilution_calculations, titration_calculations, gas_stoichiometry


ARTICLE_DIR = Path(__file__).resolve().parents[1]
SOLUTION_INPUT = ARTICLE_DIR / "data" / "solution_examples.csv"
TITRATION_INPUT = ARTICLE_DIR / "data" / "titration_examples.csv"
GAS_INPUT = ARTICLE_DIR / "data" / "gas_stoichiometry_examples.csv"
SOLUTION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "solution_dilution.csv"
TITRATION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "titration_equivalence.csv"
GAS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "gas_stoichiometry.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "solution_titration_gas.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    solutions = dilution_calculations(pd.read_csv(SOLUTION_INPUT))
    titrations = titration_calculations(pd.read_csv(TITRATION_INPUT))
    gases = gas_stoichiometry(pd.read_csv(GAS_INPUT))

    solutions.to_csv(SOLUTION_OUTPUT, index=False)
    titrations.to_csv(TITRATION_OUTPUT, index=False)
    gases.to_csv(GAS_OUTPUT, index=False)

    combined = pd.concat(
        [
            solutions.astype(str).assign(table_type="solution_dilution"),
            titrations.astype(str).assign(table_type="titration_equivalence"),
            gases.astype(str).assign(table_type="gas_stoichiometry"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Solution dilution")
    print(solutions.round(6).to_string(index=False))
    print("\nTitration equivalence")
    print(titrations.round(6).to_string(index=False))
    print("\nGas stoichiometry")
    print(gases.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
