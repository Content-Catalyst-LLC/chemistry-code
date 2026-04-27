"""
Core utilities for mathematics in chemistry workflows.

All examples are synthetic and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_GAS_CONSTANT = 8.314462618


def calculate_stoichiometry(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate product moles from stoichiometric ratios."""
    result = data.copy()
    result["product_moles"] = (
        result["reactant_moles"]
        * result["coefficient_product"]
        / result["coefficient_reactant"]
    )
    return result


def calculate_ph(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate pH from hydrogen ion activity."""
    result = data.copy()
    result["pH"] = -result["hydrogen_activity"].apply(math.log10)
    return result


def simulate_first_order(row: pd.Series) -> pd.DataFrame:
    """Simulate first-order kinetic decay."""
    rows = []
    total_time = int(row["total_time_min"])
    step = int(row["time_step_min"])
    for time in range(0, total_time + 1, step):
        concentration = float(row["initial_concentration_mol_l"]) * math.exp(
            -float(row["rate_constant_per_min"]) * time
        )
        rows.append(
            {
                "reaction": row["reaction"],
                "time_min": time,
                "concentration_mol_l": concentration,
            }
        )
    return pd.DataFrame(rows)


def calculate_equilibrium_constants(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate K from Delta G standard = -RT ln K."""
    result = data.copy()
    result["equilibrium_constant_K"] = np.exp(
        -(result["delta_g_standard_kj_mol"] * 1000.0)
        / (R_GAS_CONSTANT * result["temperature_k"])
    )
    return result


def calculate_molecular_distances(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate pairwise distances within each molecule."""
    rows = []
    for molecule, group in data.groupby("molecule"):
        group = group.reset_index(drop=True)
        coordinates = group[["x_angstrom", "y_angstrom", "z_angstrom"]].to_numpy()
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                distance = float(np.linalg.norm(coordinates[i] - coordinates[j]))
                rows.append(
                    {
                        "molecule": molecule,
                        "atom_i": group.loc[i, "atom"],
                        "atom_j": group.loc[j, "atom"],
                        "distance_angstrom": distance,
                    }
                )
    return pd.DataFrame(rows)


def summarize_matrices(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate eigenvalues for small 2x2 matrices."""
    rows = []
    for _, row in data.iterrows():
        matrix = np.array(
            [[row["a11"], row["a12"]], [row["a21"], row["a22"]]],
            dtype=float,
        )
        eigenvalues = np.linalg.eigvals(matrix)
        rows.append(
            {
                "matrix_name": row["matrix_name"],
                "eigenvalue_1": float(eigenvalues[0]),
                "eigenvalue_2": float(eigenvalues[1]),
            }
        )
    return pd.DataFrame(rows)


def summarize_uncertainty(data: pd.DataFrame, coverage_factor: float = 2.0) -> pd.DataFrame:
    """Calculate combined and expanded uncertainty."""
    combined = math.sqrt(float((data["standard_uncertainty"] ** 2).sum()))
    expanded = coverage_factor * combined
    return pd.DataFrame(
        [
            {
                "combined_standard_uncertainty": combined,
                "coverage_factor_k": coverage_factor,
                "expanded_uncertainty": expanded,
                "unit": data["unit"].iloc[0],
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
