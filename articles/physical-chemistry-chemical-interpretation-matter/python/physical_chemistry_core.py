"""
Core utilities for physical chemistry workflows.

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
F_C_MOL = 96485.33212


def thermodynamics_equilibrium(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate equilibrium constants and nonstandard free energies."""
    result = data.copy()
    result["K"] = result.apply(
        lambda row: math.exp(-(row["delta_g_standard_kj_mol"] * 1000.0) / (R_J_MOL_K * row["temperature_K"])),
        axis=1,
    )
    result["log10_K"] = result["K"].apply(math.log10)
    result["delta_g_kj_mol"] = result.apply(
        lambda row: row["delta_g_standard_kj_mol"]
        + (R_J_MOL_K * row["temperature_K"] * math.log(row["reaction_quotient"])) / 1000.0,
        axis=1,
    )
    return result


def arrhenius_kinetics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Arrhenius rate constants."""
    result = data.copy()
    result["rate_constant_s_inv"] = result.apply(
        lambda row: row["pre_exponential_s_inv"]
        * math.exp(-(row["activation_energy_kj_mol"] * 1000.0) / (R_J_MOL_K * row["temperature_K"])),
        axis=1,
    )
    result["ln_k"] = result["rate_constant_s_inv"].apply(math.log)
    return result


def boltzmann_populations(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Boltzmann populations for states at common temperature."""
    result = data.copy()
    temperature = float(result["temperature_K"].iloc[0])
    weights = np.exp(-result["energy_J"].to_numpy(dtype=float) / (KB_J_K * temperature))
    populations = weights / weights.sum()
    result["boltzmann_weight"] = weights
    result["population"] = populations
    return result


def diffusion_profile(case: pd.Series) -> pd.DataFrame:
    """Generate a one-dimensional finite-difference diffusion profile."""
    n = int(case["grid_points"])
    dx = float(case["dx"])
    dt = float(case["dt"])
    diffusion_coefficient = float(case["diffusion_coefficient"])
    steps = int(case["steps"])

    concentration = np.zeros(n)
    concentration[n // 2] = 1.0

    alpha = diffusion_coefficient * dt / (dx * dx)

    for _ in range(steps):
        updated = concentration.copy()
        for i in range(1, n - 1):
            updated[i] = concentration[i] + alpha * (
                concentration[i + 1] - 2.0 * concentration[i] + concentration[i - 1]
            )
        concentration = updated

    return pd.DataFrame(
        {
            "case_id": case["case_id"],
            "position": np.arange(n),
            "concentration": concentration,
        }
    )


def diffusion_profiles(data: pd.DataFrame) -> pd.DataFrame:
    """Generate diffusion profiles for all cases."""
    frames = [diffusion_profile(row) for _, row in data.iterrows()]
    return pd.concat(frames, ignore_index=True)


def electrochemistry_table(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Nernst potential and electrochemical free energy."""
    result = data.copy()
    result["E_V"] = result.apply(
        lambda row: row["E_standard_V"]
        - (R_J_MOL_K * row["temperature_K"] / (row["electrons_transferred"] * F_C_MOL))
        * math.log(row["reaction_quotient"]),
        axis=1,
    )
    result["delta_g_kj_mol"] = (
        -result["electrons_transferred"] * F_C_MOL * result["E_V"] / 1000.0
    )
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
