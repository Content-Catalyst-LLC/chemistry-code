"""
Calculate bond distances, distance matrices, and selected bond angles.

Run from article directory:
    python python/01_distance_matrix_and_angles.py
"""

from pathlib import Path
import pandas as pd

from geometry_core import calculate_bond_distances, calculate_angles, all_distance_matrices


ARTICLE_DIR = Path(__file__).resolve().parents[1]
COORD_INPUT = ARTICLE_DIR / "data" / "molecular_coordinates.csv"
BOND_INPUT = ARTICLE_DIR / "data" / "bonds_sample.csv"
ANGLE_INPUT = ARTICLE_DIR / "data" / "angle_definitions.csv"

DISTANCE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "bond_distances.csv"
ANGLE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "bond_angles.csv"
MATRIX_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "distance_matrices.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "distance_matrix_and_angles.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    coordinates = pd.read_csv(COORD_INPUT)
    bonds = pd.read_csv(BOND_INPUT)
    angle_definitions = pd.read_csv(ANGLE_INPUT)

    distances = calculate_bond_distances(coordinates, bonds)
    angles = calculate_angles(coordinates, angle_definitions)
    matrices = all_distance_matrices(coordinates)

    distances.to_csv(DISTANCE_OUTPUT, index=False)
    angles.to_csv(ANGLE_OUTPUT, index=False)
    matrices.to_csv(MATRIX_OUTPUT, index=False)

    combined = pd.concat(
        [
            distances.astype(str).assign(table_type="bond_distances"),
            angles.astype(str).assign(table_type="bond_angles"),
            matrices.astype(str).assign(table_type="distance_matrix"),
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Bond distances")
    print(distances.round(6).to_string(index=False))
    print("\nBond angles")
    print(angles.round(3).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
