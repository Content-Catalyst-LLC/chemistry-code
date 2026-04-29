"""
Core utilities for quantum chemistry and electronic structure workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618
KB_J_K = 1.380649e-23
H_J_S = 6.62607015e-34
HARTREE_TO_KJ_MOL = 2625.49962


def orbital_mixing(data: pd.DataFrame) -> pd.DataFrame:
    """Solve two-level orbital mixing cases."""
    rows = []

    for _, row in data.iterrows():
        hamiltonian = np.array(
            [
                [row["energy_a"], row["coupling"]],
                [row["coupling"], row["energy_b"]],
            ],
            dtype=float,
        )
        energies, coeffs = np.linalg.eigh(hamiltonian)

        for index, energy in enumerate(energies):
            rows.append(
                {
                    "case_id": row["case_id"],
                    "orbital": f"MO_{index + 1}",
                    "energy_units": energy,
                    "coefficient_basis_a": coeffs[0, index],
                    "coefficient_basis_b": coeffs[1, index],
                    "basis_a_weight": coeffs[0, index] ** 2,
                    "basis_b_weight": coeffs[1, index] ** 2,
                }
            )

    return pd.DataFrame(rows)


def electron_density(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate a simple one-dimensional electron-density scaffold."""
    result = data.copy()
    result["density"] = (
        result["occupancy_1"] * result["orbital_1"] ** 2
        + result["occupancy_2"] * result["orbital_2"] ** 2
    )
    return result


def huckel_levels(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple Hückel energy levels for linear chains."""
    rows = []

    for _, row in data.iterrows():
        n = int(row["sites"])
        alpha = float(row["alpha"])
        beta = float(row["beta"])

        h = np.zeros((n, n))
        for i in range(n):
            h[i, i] = alpha
            if i < n - 1:
                h[i, i + 1] = beta
                h[i + 1, i] = beta

        energies = np.linalg.eigvalsh(h)

        for level, energy in enumerate(energies, start=1):
            rows.append(
                {
                    "system": row["system"],
                    "level": level,
                    "energy_units": energy,
                    "sites": n,
                }
            )

    return pd.DataFrame(rows)


def basis_convergence(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate relative energies and convergence increments."""
    frames = []

    for case_id, group in data.groupby("case_id"):
        temp = group.copy()
        temp["relative_energy_kj_mol"] = (
            temp["energy_hartree"] - temp["energy_hartree"].min()
        ) * HARTREE_TO_KJ_MOL
        temp["energy_change_from_previous_kj_mol"] = (
            temp["energy_hartree"].diff() * HARTREE_TO_KJ_MOL
        )
        frames.append(temp)

    return pd.concat(frames, ignore_index=True)


def spin_state_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize spin-state ordering."""
    result = data.copy()
    result["ground_state_hint"] = (
        result.groupby("complex")["relative_energy_kj_mol"].transform("min")
        == result["relative_energy_kj_mol"]
    ).astype(int)
    return result


def excited_state_populations(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Boltzmann populations for electronic-state scaffold."""
    result = data.copy()
    temperature = float(result["temperature_K"].iloc[0])
    weights = np.exp(
        -(result["relative_energy_kj_mol"].to_numpy(dtype=float) * 1000.0)
        / (R_J_MOL_K * temperature)
    )
    result["boltzmann_weight"] = weights
    result["population"] = weights / weights.sum()
    return result


def transition_state_theory(data: pd.DataFrame) -> pd.DataFrame:
    """Estimate rates from transition-state theory."""
    result = data.copy()
    result["rate_s_inv"] = result.apply(
        lambda row: (KB_J_K * row["temperature_K"] / H_J_S)
        * math.exp(-(row["activation_free_energy_kj_mol"] * 1000.0) / (R_J_MOL_K * row["temperature_K"])),
        axis=1,
    )
    result["log10_rate"] = result["rate_s_inv"].apply(math.log10)
    return result


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
