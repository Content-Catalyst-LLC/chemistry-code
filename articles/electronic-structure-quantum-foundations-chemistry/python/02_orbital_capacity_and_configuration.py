"""
Summarize orbital capacities, electron configurations, and effective nuclear charge.

Run from article directory:
    python python/02_orbital_capacity_and_configuration.py
"""

from pathlib import Path
import pandas as pd

from electronic_structure_core import orbital_capacities, effective_nuclear_charge


ARTICLE_DIR = Path(__file__).resolve().parents[1]
ORBITAL_INPUT = ARTICLE_DIR / "data" / "orbitals_sample.csv"
CONFIG_INPUT = ARTICLE_DIR / "data" / "electron_configurations_sample.csv"
ZEFF_INPUT = ARTICLE_DIR / "data" / "effective_nuclear_charge_sample.csv"
ORBITAL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "orbital_capacities.csv"
CONFIG_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "electron_configurations.csv"
ZEFF_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "effective_nuclear_charge.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "orbital_capacity_and_configuration.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    orbitals = orbital_capacities(pd.read_csv(ORBITAL_INPUT))
    configs = pd.read_csv(CONFIG_INPUT)
    zeff = effective_nuclear_charge(pd.read_csv(ZEFF_INPUT))

    orbitals.to_csv(ORBITAL_OUTPUT, index=False)
    configs.to_csv(CONFIG_OUTPUT, index=False)
    zeff.to_csv(ZEFF_OUTPUT, index=False)

    combined = pd.concat(
        [
            orbitals.astype(str).assign(table_type="orbital_capacities"),
            configs.astype(str).assign(table_type="electron_configurations"),
            zeff.astype(str).assign(table_type="effective_nuclear_charge"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Orbital capacities")
    print(orbitals.to_string(index=False))
    print("\nElectron configurations")
    print(configs.to_string(index=False))
    print("\nEffective nuclear charge")
    print(zeff.round(3).to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
