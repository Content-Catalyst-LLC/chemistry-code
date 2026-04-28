"""
Core utilities for oxidation, reduction, and electron-transfer workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618
F_C_MOL = 96485.33212


def cell_potential_gibbs(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate standard cell potential, Gibbs free energy, and equilibrium constant."""
    result = data.copy()
    result["E_cell_standard_V"] = result["E_cathode_V"] - result["E_anode_V"]
    result["delta_g_standard_kj_mol"] = (
        -result["electrons_transferred"] * F_C_MOL * result["E_cell_standard_V"] / 1000.0
    )
    result["ln_K_29815"] = (
        result["electrons_transferred"] * F_C_MOL * result["E_cell_standard_V"]
        / (R_J_MOL_K * 298.15)
    )
    result["log10_K_29815"] = result["ln_K_29815"] / math.log(10.0)
    return result


def nernst_equation(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate redox potential under nonstandard conditions."""
    result = data.copy()
    result["E_V"] = result.apply(
        lambda row: row["E_standard_V"]
        - (
            R_J_MOL_K
            * row["temperature_K"]
            / (row["electrons_transferred"] * F_C_MOL)
        )
        * math.log(row["reaction_quotient"]),
        axis=1,
    )
    result["potential_shift_V"] = result["E_V"] - result["E_standard_V"]
    return result


def redox_titration(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate titrant moles and volume from electron equivalence."""
    result = data.copy()
    result["titrant_moles_required"] = (
        result["analyte_moles"] * result["electrons_donated_per_analyte"]
    ) / result["electrons_accepted_per_titrant"]
    result["titrant_volume_l"] = (
        result["titrant_moles_required"] / result["titrant_concentration_mol_l"]
    )
    result["titrant_volume_ml"] = result["titrant_volume_l"] * 1000.0
    return result


def ph_dependent_redox(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate simplified pH-dependent redox potential profiles.

    For a generic reduction:
    Ox + mH+ + ne- -> Red

    Q contribution from protons is approximated as 1/[H+]^m.
    """
    rows = []

    for _, row in data.iterrows():
        pH_values = np.arange(row["pH_min"], row["pH_max"] + row["pH_step"], row["pH_step"])

        for ph in pH_values:
            h_activity = 10.0 ** (-ph)
            q_value = 1.0 / (h_activity ** row["protons_transferred"])
            e_value = row["E_standard_V"] - (
                R_J_MOL_K
                * row["temperature_K"]
                / (row["electrons_transferred"] * F_C_MOL)
            ) * math.log(q_value)

            rows.append(
                {
                    "case_id": row["case_id"],
                    "pH": float(ph),
                    "E_V": e_value,
                    "E_standard_V": row["E_standard_V"],
                    "electrons_transferred": row["electrons_transferred"],
                    "protons_transferred": row["protons_transferred"],
                }
            )

    return pd.DataFrame(rows)


def corrosion_pair_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """Estimate galvanic direction from standard reduction potentials."""
    rows = []

    for _, row in data.iterrows():
        if row["E_reduction_a_V"] < row["E_reduction_b_V"]:
            anodic = row["metal_a"]
            cathodic = row["metal_b"]
            e_cell = row["E_reduction_b_V"] - row["E_reduction_a_V"]
        else:
            anodic = row["metal_b"]
            cathodic = row["metal_a"]
            e_cell = row["E_reduction_a_V"] - row["E_reduction_b_V"]

        rows.append(
            {
                "case_id": row["case_id"],
                "anodic_material_more_likely_oxidized": anodic,
                "cathodic_material_more_likely_reduced": cathodic,
                "simplified_E_cell_V": e_cell,
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
