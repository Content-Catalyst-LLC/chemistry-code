"""
Core utilities for molecular geometry, symmetry, and structure workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def vector_from_row(row: pd.Series) -> np.ndarray:
    """Return coordinate vector from a coordinate row."""
    return row[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)


def calculate_bond_distances(coordinates: pd.DataFrame, bonds: pd.DataFrame) -> pd.DataFrame:
    """Calculate bond distances from atom coordinates."""
    rows = []

    for _, bond in bonds.iterrows():
        molecule = bond["molecule"]
        group = coordinates[coordinates["molecule"] == molecule].set_index("atom")

        atom_i = bond["atom_i"]
        atom_j = bond["atom_j"]

        ri = vector_from_row(group.loc[atom_i])
        rj = vector_from_row(group.loc[atom_j])

        rows.append(
            {
                "molecule": molecule,
                "atom_i": atom_i,
                "atom_j": atom_j,
                "bond_type": bond["bond_type"],
                "distance_angstrom": float(np.linalg.norm(ri - rj)),
            }
        )

    return pd.DataFrame(rows)


def calculate_angle(coordinates: pd.DataFrame, molecule: str, atom_a: str, atom_b: str, atom_c: str) -> float:
    """Calculate angle A-B-C in degrees."""
    group = coordinates[coordinates["molecule"] == molecule].set_index("atom")
    ra = vector_from_row(group.loc[atom_a])
    rb = vector_from_row(group.loc[atom_b])
    rc = vector_from_row(group.loc[atom_c])

    u = ra - rb
    v = rc - rb

    cos_theta = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.degrees(math.acos(cos_theta))


def calculate_angles(coordinates: pd.DataFrame, angle_definitions: pd.DataFrame) -> pd.DataFrame:
    """Calculate selected molecular bond angles."""
    rows = []
    for _, row in angle_definitions.iterrows():
        rows.append(
            {
                "molecule": row["molecule"],
                "angle_name": row["angle_name"],
                "angle_degrees": calculate_angle(
                    coordinates,
                    row["molecule"],
                    row["atom_a"],
                    row["atom_b"],
                    row["atom_c"],
                ),
            }
        )
    return pd.DataFrame(rows)


def distance_matrix_for_molecule(coordinates: pd.DataFrame, molecule: str) -> pd.DataFrame:
    """Create long-form distance matrix entries for one molecule."""
    group = coordinates[coordinates["molecule"] == molecule].reset_index(drop=True)
    coords = group[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)

    rows = []
    for i in range(len(group)):
        for j in range(len(group)):
            rows.append(
                {
                    "molecule": molecule,
                    "atom_i": group.loc[i, "atom"],
                    "atom_j": group.loc[j, "atom"],
                    "distance_angstrom": float(np.linalg.norm(coords[i] - coords[j])),
                }
            )

    return pd.DataFrame(rows)


def all_distance_matrices(coordinates: pd.DataFrame) -> pd.DataFrame:
    """Create long-form distance matrix entries for all molecules."""
    return pd.concat(
        [distance_matrix_for_molecule(coordinates, molecule) for molecule in coordinates["molecule"].unique()],
        ignore_index=True,
    )


def centers_and_extents(coordinates: pd.DataFrame) -> pd.DataFrame:
    """Calculate centers of geometry, centers of mass, and maximum radial extent."""
    rows = []

    for molecule, group in coordinates.groupby("molecule"):
        coords = group[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)
        masses = group["mass_u"].to_numpy(dtype=float)

        center_geometry = coords.mean(axis=0)
        center_mass = (masses[:, None] * coords).sum(axis=0) / masses.sum()
        distances_from_cm = np.linalg.norm(coords - center_mass, axis=1)

        rows.append(
            {
                "molecule": molecule,
                "center_geometry_x": float(center_geometry[0]),
                "center_geometry_y": float(center_geometry[1]),
                "center_geometry_z": float(center_geometry[2]),
                "center_mass_x": float(center_mass[0]),
                "center_mass_y": float(center_mass[1]),
                "center_mass_z": float(center_mass[2]),
                "max_extent_from_center_mass": float(distances_from_cm.max()),
            }
        )

    return pd.DataFrame(rows)


def rotation_matrix_z(angle_degrees: float) -> np.ndarray:
    """Create a z-axis rotation matrix."""
    theta = math.radians(angle_degrees)
    return np.array(
        [
            [math.cos(theta), -math.sin(theta), 0.0],
            [math.sin(theta), math.cos(theta), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )


def apply_rotation_example() -> pd.DataFrame:
    """Apply a 120-degree rotation to a triangular coordinate set."""
    coords = pd.DataFrame(
        {
            "atom": ["A", "B", "C"],
            "x_angstrom": [1.0, -0.5, -0.5],
            "y_angstrom": [0.0, 0.8660254, -0.8660254],
            "z_angstrom": [0.0, 0.0, 0.0],
        }
    )
    rotation = rotation_matrix_z(120.0)
    rotated = coords[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float) @ rotation.T

    result = coords.copy()
    result["x_rotated"] = rotated[:, 0]
    result["y_rotated"] = rotated[:, 1]
    result["z_rotated"] = rotated[:, 2]
    return result


def conformer_rmsd(conformers: pd.DataFrame) -> pd.DataFrame:
    """Calculate RMSD between conformers A and B with matching atom labels."""
    a = conformers[conformers["conformer"] == "A"].sort_values("atom")
    b = conformers[conformers["conformer"] == "B"].sort_values("atom")

    coords_a = a[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)
    coords_b = b[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)

    rmsd = math.sqrt(float(np.mean(np.sum((coords_a - coords_b) ** 2, axis=1))))

    return pd.DataFrame(
        [
            {
                "conformer_a": "A",
                "conformer_b": "B",
                "rmsd_angstrom": rmsd,
            }
        ]
    )


def sha256_file(path: Path) -> str:
    """Calculate SHA-256 checksum for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_sha256(path: Path) -> str:
    """Return a checksum or not-available marker."""
    if path.exists() and path.is_file():
        return sha256_file(path)
    return "not_available"


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Convert a small DataFrame to markdown without external dependencies."""
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(lines)
