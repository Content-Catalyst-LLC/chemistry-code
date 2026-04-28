"""
Calculate bond distances and selected bond angles.

Run from article directory:
    python python/01_bond_geometry.py
"""

from pathlib import Path
import pandas as pd

from bonding_core import calculate_bond_distances, calculate_water_angle


ARTICLE_DIR = Path(__file__).resolve().parents[1]
COORD_INPUT = ARTICLE_DIR / "data" / "molecular_coordinates.csv"
BOND_INPUT = ARTICLE_DIR / "data" / "bonds_sample.csv"
DIST_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "bond_distances.csv"
ANGLE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "bond_angles.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "bond_geometry.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    coordinates = pd.read_csv(COORD_INPUT)
    bonds = pd.read_csv(BOND_INPUT)

    distances = calculate_bond_distances(coordinates, bonds)
    angles = calculate_water_angle(coordinates)

    distances.to_csv(DIST_OUTPUT, index=False)
    angles.to_csv(ANGLE_OUTPUT, index=False)

    combined = pd.concat(
        [
            distances.astype(str).assign(table_type="bond_distance"),
            angles.astype(str).assign(table_type="bond_angle"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Bond distances")
    print(distances.round(6).to_string(index=False))
    print("\nBond angles")
    print(angles.round(3).to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
