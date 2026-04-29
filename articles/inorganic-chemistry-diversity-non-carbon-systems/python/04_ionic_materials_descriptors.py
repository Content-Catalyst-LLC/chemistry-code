"""
Generate ionic solid, perovskite, and materials descriptor scaffolds.

Run from article directory:
    python python/04_ionic_materials_descriptors.py
"""

from pathlib import Path
import pandas as pd

from inorganic_core import ionic_solid_descriptors, perovskite_tolerance, material_descriptor_table


ARTICLE_DIR = Path(__file__).resolve().parents[1]
IONIC_INPUT = ARTICLE_DIR / "data" / "ionic_solid_cases.csv"
PEROV_INPUT = ARTICLE_DIR / "data" / "perovskite_cases.csv"
MAT_INPUT = ARTICLE_DIR / "data" / "material_descriptor_cases.csv"

IONIC_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "ionic_solid_descriptors.csv"
PEROV_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "perovskite_tolerance.csv"
MAT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "material_descriptor_table.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "ionic_materials_descriptors.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    ionic = ionic_solid_descriptors(pd.read_csv(IONIC_INPUT))
    perovskites = perovskite_tolerance(pd.read_csv(PEROV_INPUT))
    materials = material_descriptor_table(pd.read_csv(MAT_INPUT))

    ionic.to_csv(IONIC_OUTPUT, index=False)
    perovskites.to_csv(PEROV_OUTPUT, index=False)
    materials.to_csv(MAT_OUTPUT, index=False)

    combined = pd.concat(
        [
            ionic.astype(str).assign(table_type="ionic_solid_descriptors"),
            perovskites.astype(str).assign(table_type="perovskite_tolerance"),
            materials.astype(str).assign(table_type="material_descriptor_table"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Ionic solid descriptors")
    print(ionic.round(6).to_string(index=False))
    print("\nPerovskite tolerance")
    print(perovskites.round(6).to_string(index=False))
    print("\nMaterials descriptor table")
    print(materials.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
