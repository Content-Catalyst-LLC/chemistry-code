"""
Core utilities for electronic structure and quantum foundations of chemistry.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib

import numpy as np
import pandas as pd


H = 6.62607015e-34
C = 299792458.0
EV_TO_J = 1.602176634e-19
ELECTRON_MASS = 9.1093837139e-31


def hydrogen_energy_levels(max_n: int = 6) -> pd.DataFrame:
    """Calculate approximate hydrogen energy levels using E_n = -13.6 eV / n^2."""
    rows = []
    for n in range(1, max_n + 1):
        energy_eV = -13.6 / (n ** 2)
        rows.append(
            {
                "n": n,
                "energy_eV": energy_eV,
                "energy_J": energy_eV * EV_TO_J,
            }
        )
    return pd.DataFrame(rows)


def hydrogen_transitions_to_ground(max_n: int = 6) -> pd.DataFrame:
    """Calculate photon wavelengths for transitions from n > 1 to n = 1."""
    levels = hydrogen_energy_levels(max_n)
    ground_energy = float(levels.loc[levels["n"] == 1, "energy_J"].iloc[0])

    rows = []
    for n_initial in range(2, max_n + 1):
        initial_energy = float(levels.loc[levels["n"] == n_initial, "energy_J"].iloc[0])
        delta_energy = abs(initial_energy - ground_energy)
        wavelength_m = H * C / delta_energy
        rows.append(
            {
                "transition": f"{n_initial}_to_1",
                "delta_energy_eV": delta_energy / EV_TO_J,
                "wavelength_nm": wavelength_m * 1.0e9,
            }
        )

    return pd.DataFrame(rows)


def orbital_capacities(orbitals: pd.DataFrame) -> pd.DataFrame:
    """Calculate orbital count and maximum electron count for each subshell."""
    result = orbitals.copy()
    result["orbital_count"] = 2 * result["l"] + 1
    result["maximum_electrons"] = 2 * result["orbital_count"]
    return result


def effective_nuclear_charge(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate approximate effective nuclear charge from Z_eff = Z - S."""
    result = data.copy()
    result["effective_nuclear_charge"] = (
        result["atomic_number"] - result["shielding_constant"]
    )
    return result


def particle_in_box_levels(box_length_nm: float, max_n: int = 6) -> pd.DataFrame:
    """Calculate 1D particle-in-a-box energy levels for an electron."""
    length_m = box_length_nm * 1.0e-9
    rows = []
    for n in range(1, max_n + 1):
        energy_J = (n ** 2 * H ** 2) / (8.0 * ELECTRON_MASS * length_m ** 2)
        rows.append(
            {
                "box_length_nm": box_length_nm,
                "n": n,
                "energy_J": energy_J,
                "energy_eV": energy_J / EV_TO_J,
            }
        )
    return pd.DataFrame(rows)


def particle_in_box_table(examples: pd.DataFrame) -> pd.DataFrame:
    """Calculate particle-in-a-box levels for multiple box lengths."""
    tables = []
    for _, row in examples.iterrows():
        tables.append(
            particle_in_box_levels(
                box_length_nm=float(row["box_length_nm"]),
                max_n=int(row["max_n"]),
            ).assign(system=row["system"])
        )
    return pd.concat(tables, ignore_index=True)


def hamiltonian_eigenvalues(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate eigenvalues for 3x3 Hamiltonian-style matrices."""
    rows = []
    for _, row in data.iterrows():
        matrix = np.array(
            [
                [row["h11"], row["h12"], row["h13"]],
                [row["h21"], row["h22"], row["h23"]],
                [row["h31"], row["h32"], row["h33"]],
            ],
            dtype=float,
        )
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        rows.append(
            {
                "matrix_name": row["matrix_name"],
                "energy_1": float(eigenvalues[0]),
                "energy_2": float(eigenvalues[1]),
                "energy_3": float(eigenvalues[2]),
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
