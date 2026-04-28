"""
Core utilities for chemical thermodynamics and energetics workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618


def calorimetry_enthalpy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate heat transfer and molar reaction enthalpy from calorimetry data."""
    result = data.copy()
    result["q_solution_j"] = (
        result["solution_mass_g"]
        * result["specific_heat_j_g_k"]
        * result["temperature_change_k"]
    )
    result["q_calorimeter_j"] = (
        result["calorimeter_heat_capacity_j_k"] * result["temperature_change_k"]
    )
    result["q_surroundings_j"] = result["q_solution_j"] + result["q_calorimeter_j"]
    result["q_reaction_j"] = -result["q_surroundings_j"]
    result["delta_h_reaction_kj_mol"] = (
        result["q_reaction_j"] / 1000.0 / result["reaction_amount_mol"]
    )
    return result


def hess_law_reaction_enthalpy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate reaction enthalpy from formation enthalpy contributions."""
    result = data.copy()
    result["contribution_kj_mol"] = (
        result["coefficient"] * result["delta_h_f_kj_mol"]
    )

    summary = (
        result.groupby("reaction_id", as_index=False)
        .agg(delta_h_reaction_kj_mol=("contribution_kj_mol", "sum"))
        .sort_values("reaction_id")
    )
    return result, summary


def gibbs_equilibrium(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Gibbs free energy, standard equilibrium constants,
    and nonstandard free energy.
    """
    result = data.copy()
    result["delta_g_standard_kj_mol"] = (
        result["delta_h_kj_mol"]
        - result["temperature_k"] * result["delta_s_j_mol_k"] / 1000.0
    )

    result["equilibrium_constant"] = np.exp(
        -(result["delta_g_standard_kj_mol"] * 1000.0)
        / (R_J_MOL_K * result["temperature_k"])
    )

    result["delta_g_nonstandard_kj_mol"] = (
        result["delta_g_standard_kj_mol"]
        + (R_J_MOL_K * result["temperature_k"] * np.log(result["reaction_quotient"])) / 1000.0
    )

    result["log10_equilibrium_constant"] = np.log10(result["equilibrium_constant"])
    return result


def vant_hoff_fit(data: pd.DataFrame) -> pd.DataFrame:
    """Fit ln K versus 1/T to estimate thermodynamic quantities."""
    rows = []

    for reaction, group in data.groupby("reaction"):
        group = group.copy()
        group["inverse_temperature_k_inv"] = 1.0 / group["temperature_k"]
        group["ln_k"] = np.log(group["equilibrium_constant"])

        slope, intercept = np.polyfit(
            group["inverse_temperature_k_inv"],
            group["ln_k"],
            deg=1,
        )

        delta_h_j_mol = -slope * R_J_MOL_K
        delta_s_j_mol_k = intercept * R_J_MOL_K

        rows.append(
            {
                "reaction": reaction,
                "slope": float(slope),
                "intercept": float(intercept),
                "estimated_delta_h_kj_mol": float(delta_h_j_mol / 1000.0),
                "estimated_delta_s_j_mol_k": float(delta_s_j_mol_k),
            }
        )

    return pd.DataFrame(rows)


def phase_transition_entropy(data: pd.DataFrame) -> pd.DataFrame:
    """Compare tabulated entropy changes with Delta H / T estimates."""
    result = data.copy()
    result["estimated_entropy_change_j_mol_k"] = (
        result["delta_h_transition_kj_mol"] * 1000.0 / result["temperature_k"]
    )
    result["entropy_difference_j_mol_k"] = (
        result["estimated_entropy_change_j_mol_k"]
        - result["entropy_change_j_mol_k"]
    )
    return result


def coupled_reactions(data: pd.DataFrame) -> pd.DataFrame:
    """Sum free-energy changes for coupled reaction cases."""
    return (
        data.groupby("coupling_case", as_index=False)
        .agg(
            total_delta_g_kj_mol=("delta_g_kj_mol", "sum"),
            step_count=("step", "count"),
        )
        .sort_values("coupling_case")
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
