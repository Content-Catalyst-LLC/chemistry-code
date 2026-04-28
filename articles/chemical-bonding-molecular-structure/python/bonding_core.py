"""
Core utilities for chemical bonding and molecular structure workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def calculate_bond_distances(coordinates: pd.DataFrame, bonds: pd.DataFrame) -> pd.DataFrame:
    """Calculate bond distances from atom coordinates."""
    rows = []

    for _, bond in bonds.iterrows():
        molecule = bond["molecule"]
        group = coordinates[coordinates["molecule"] == molecule].set_index("atom")

        atom_i = bond["atom_i"]
        atom_j = bond["atom_j"]

        ri = group.loc[atom_i, ["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)
        rj = group.loc[atom_j, ["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)

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


def calculate_water_angle(coordinates: pd.DataFrame) -> pd.DataFrame:
    """Calculate the H-O-H bond angle for the water example."""
    group = coordinates[coordinates["molecule"] == "water"].set_index("atom")
    oxygen = group.loc["O", ["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)
    h1 = group.loc["H1", ["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)
    h2 = group.loc["H2", ["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)

    u = h1 - oxygen
    v = h2 - oxygen

    cos_angle = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return pd.DataFrame(
        [
            {
                "molecule": "water",
                "angle": "H-O-H",
                "angle_degrees": math.degrees(math.acos(cos_angle)),
            }
        ]
    )


def classify_bond_polarity(delta_chi: float) -> str:
    """Classify bond polarity using simplified educational thresholds."""
    if delta_chi < 0.4:
        return "weakly polar or nearly nonpolar covalent"
    if delta_chi < 1.7:
        return "polar covalent"
    return "strongly polar or ionic model useful"


def calculate_bond_polarity(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate electronegativity difference and simplified bond classification."""
    result = data.copy()
    result["delta_chi"] = (result["chi_a"] - result["chi_b"]).abs()
    result["simplified_classification"] = result["delta_chi"].apply(classify_bond_polarity)
    return result


def calculate_formal_charge(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate formal charge from valence, nonbonding, and bonding electrons."""
    result = data.copy()
    result["formal_charge"] = (
        result["valence_electrons"]
        - result["nonbonding_electrons"]
        - result["bonding_electrons"] / 2.0
    )
    return result


def calculate_mo_bond_order(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple molecular-orbital bond order."""
    result = data.copy()
    result["bond_order"] = (
        result["bonding_electrons"] - result["antibonding_electrons"]
    ) / 2.0
    return result


def estimate_dipole_vectors(coordinates: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate simple dipole vectors using partial charges and coordinates.

    This educational estimate assumes coordinates in angstroms and charge in
    elementary-charge units. It is not a production dipole calculation.
    """
    rows = []
    for molecule, group in coordinates.groupby("molecule"):
        positions = group[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy(dtype=float)
        charges = group["partial_charge"].to_numpy(dtype=float)
        dipole = (charges[:, None] * positions).sum(axis=0)
        magnitude = float(np.linalg.norm(dipole))

        rows.append(
            {
                "molecule": molecule,
                "dipole_x_e_angstrom": float(dipole[0]),
                "dipole_y_e_angstrom": float(dipole[1]),
                "dipole_z_e_angstrom": float(dipole[2]),
                "dipole_magnitude_e_angstrom": magnitude,
            }
        )

    return pd.DataFrame(rows)


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
