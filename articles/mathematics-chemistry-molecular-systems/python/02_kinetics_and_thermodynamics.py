"""
Simulate kinetics and calculate equilibrium constants.

Run from article directory:
    python python/02_kinetics_and_thermodynamics.py
"""

from pathlib import Path
import pandas as pd

from math_chemistry_core import simulate_first_order, calculate_equilibrium_constants


ARTICLE_DIR = Path(__file__).resolve().parents[1]
KINETICS_PATH = ARTICLE_DIR / "data" / "kinetics_examples.csv"
THERMO_PATH = ARTICLE_DIR / "data" / "thermodynamics_examples.csv"
KINETICS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "kinetics_trajectories.csv"
THERMO_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "thermodynamics_equilibrium.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "kinetics_and_thermodynamics.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    kinetics_examples = pd.read_csv(KINETICS_PATH)
    trajectories = pd.concat(
        [simulate_first_order(row) for _, row in kinetics_examples.iterrows()],
        ignore_index=True,
    )

    thermo = calculate_equilibrium_constants(pd.read_csv(THERMO_PATH))

    trajectories.to_csv(KINETICS_OUTPUT, index=False)
    thermo.to_csv(THERMO_OUTPUT, index=False)

    combined = pd.concat(
        [
            trajectories.astype(str).assign(table_type="kinetics"),
            thermo.astype(str).assign(table_type="thermodynamics"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Kinetics")
    print(trajectories.round(6).to_string(index=False))
    print("\nThermodynamics")
    print(thermo.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
