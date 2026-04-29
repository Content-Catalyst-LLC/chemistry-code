"""
Core utilities for catalysis and chemical pathway-control workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618


def barrier_rate_enhancement(data: pd.DataFrame) -> pd.DataFrame:
    """Estimate rate enhancement from catalytic barrier lowering."""
    result = data.copy()
    result["rate_enhancement_estimate"] = result.apply(
        lambda row: math.exp((row["delta_Ea_kJ_mol"] * 1000.0) / (R_J_MOL_K * row["temperature_K"])),
        axis=1,
    )
    result["log10_rate_enhancement"] = np.log10(result["rate_enhancement_estimate"])
    return result


def turnover_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate turnover number, turnover frequency, and catalytic activity."""
    result = data.copy()
    result["TON"] = result["product_mol"] / result["catalyst_mol"]
    result["TOF_s_inv"] = result["TON"] / result["time_s"]
    result["catalytic_activity_mol_s"] = result["product_mol"] / result["time_s"]
    return result


def adsorption_surface_rates(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Langmuir coverages and a simplified Langmuir-Hinshelwood rate."""
    result = data.copy()
    result["theta_A"] = (result["K_A"] * result["pressure"]) / (1.0 + result["K_A"] * result["pressure"])
    result["theta_B"] = (result["K_B"] * result["pressure"]) / (1.0 + result["K_B"] * result["pressure"])
    result["surface_rate"] = result["k_surface"] * result["theta_A"] * result["theta_B"]
    return result


def michaelis_menten_rates(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Michaelis-Menten catalytic rates."""
    result = data.copy()
    result["rate_umol_min"] = (
        result["Vmax_umol_min"] * result["substrate_mM"]
    ) / (result["Km_mM"] + result["substrate_mM"])
    result["fraction_of_vmax"] = result["rate_umol_min"] / result["Vmax_umol_min"]
    return result


def catalytic_cycle_simulation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate a simplified catalyst binding and product formation cycle.

    C + S <=> CS
    CS -> C + P

    Euler integration is used for educational transparency.
    """
    rows = []

    for _, row in data.iterrows():
        c_free = float(row["catalyst_total_mol_l"])
        cs = 0.0
        s = float(row["substrate_initial_mol_l"])
        p = 0.0

        times = np.arange(0, row["total_time_s"] + row["time_step_s"], row["time_step_s"])
        dt = float(row["time_step_s"])

        for t in times:
            rows.append(
                {
                    "case_id": row["case_id"],
                    "time_s": float(t),
                    "catalyst_free_mol_l": c_free,
                    "catalyst_substrate_complex_mol_l": cs,
                    "substrate_mol_l": s,
                    "product_mol_l": p,
                }
            )

            bind = row["k_bind"] * c_free * s
            release = row["k_release"] * cs
            product = row["k_product"] * cs

            c_free_next = c_free - bind * dt + release * dt + product * dt
            cs_next = cs + bind * dt - release * dt - product * dt
            s_next = max(s - bind * dt + release * dt, 0.0)
            p_next = p + product * dt

            c_free = max(c_free_next, 0.0)
            cs = max(cs_next, 0.0)
            s = s_next
            p = p_next

    return pd.DataFrame(rows)


def deactivation_profiles(data: pd.DataFrame) -> pd.DataFrame:
    """Generate exponential catalyst activity decay profiles."""
    rows = []

    for _, row in data.iterrows():
        times = np.arange(0, row["total_time_s"] + row["time_step_s"], row["time_step_s"])

        for t in times:
            activity = row["initial_activity"] * math.exp(-row["decay_constant_per_s"] * t)
            rows.append(
                {
                    "case_id": row["case_id"],
                    "time_s": float(t),
                    "relative_activity": activity,
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
