"""
Generate simple structure-property descriptor scaffolds.

Run from article directory:
    python python/04_structure_property_scaffold.py
"""

from pathlib import Path
import pandas as pd

from organic_structure_core import structure_property_scaffold, boltzmann_population


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "structure_property_cases.csv"
PROPERTY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "structure_property_scaffold_only.csv"
CONFORMER_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "conformer_populations.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "structure_property_scaffold.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    property_table = structure_property_scaffold(pd.read_csv(INPUT_PATH))
    conformers = boltzmann_population([0.0, 2.5, 6.0, 11.0], temperature_k=298.15)

    property_table.to_csv(PROPERTY_OUTPUT, index=False)
    conformers.to_csv(CONFORMER_OUTPUT, index=False)

    combined = pd.concat(
        [
            property_table.astype(str).assign(table_type="structure_property_scaffold"),
            conformers.astype(str).assign(table_type="conformer_population"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Structure-property scaffold")
    print(property_table.to_string(index=False))
    print("\nConformer populations")
    print(conformers.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
