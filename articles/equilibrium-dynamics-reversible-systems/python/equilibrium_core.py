"""
Core utilities for chemical equilibrium and reversible-system workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618


def reaction_quotient_free_energy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate reaction quotient, Q/K direction, and Delta G from Q/K."""
    rows = []

    for _, row in data.iterrows():
        reactant_term = (row["A_mol_l"] ** row["stoich_A"]) * (row["B_mol_l"] ** row["stoich_B"])
        product_term = row["C_mol_l"] ** row["stoich_C"]

        if row["stoich_D"] > 0:
            product_term *= row["D_mol_l"] ** row["stoich_D"]

        q_value = product_term / reactant_term
        delta_g_kj_mol = R_J_MOL_K * row["temperature_K"] * math.log(q_value / row["K"]) / 1000.0

        if q_value < row["K"]:
            direction = "net forward"
        elif q_value > row["K"]:
            direction = "net reverse"
        else:
            direction = "at equilibrium"

        rows.append(
            {
                "case_id": row["case_id"],
                "reaction": row["reaction"],
                "K": row["K"],
                "Q": q_value,
                "Q_over_K": q_value / row["K"],
                "delta_g_kj_mol": delta_g_kj_mol,
                "predicted_direction": direction,
            }
        )

    return pd.DataFrame(rows)


def solve_simple_isomerization(data: pd.DataFrame) -> pd.DataFrame:
    """Solve A <=> B with K = B/A and mass balance A + B = total."""
    rows = []

    for _, row in data.iterrows():
        total = row["total_concentration_mol_l"]
        k_value = row["K"]

        a_eq = total / (1.0 + k_value)
        b_eq = total - a_eq

        rows.append(
            {
                "case_id": row["case_id"],
                "reaction": row["reaction"],
                "K": k_value,
                "total_concentration_mol_l": total,
                "A_eq_mol_l": a_eq,
                "B_eq_mol_l": b_eq,
                "Q_eq": b_eq / a_eq,
            }
        )

    return pd.DataFrame(rows)


def simulate_reversible_dynamics(data: pd.DataFrame) -> pd.DataFrame:
    """Simulate A <=> B using transparent Euler integration."""
    rows = []

    for _, row in data.iterrows():
        time_values = np.arange(0, row["total_time_min"] + row["time_step_min"], row["time_step_min"])

        a = float(row["A0_mol_l"])
        b = float(row["B0_mol_l"])
        dt = float(row["time_step_min"])

        for t in time_values:
            q_value = b / a if a > 0 else math.inf
            rows.append(
                {
                    "case_id": row["case_id"],
                    "time_min": float(t),
                    "A_mol_l": a,
                    "B_mol_l": b,
                    "Q": q_value,
                    "expected_K_from_kf_kr": row["kf_per_min"] / row["kr_per_min"],
                }
            )

            forward_rate = row["kf_per_min"] * a
            reverse_rate = row["kr_per_min"] * b
            net_rate = forward_rate - reverse_rate

            a = max(a - net_rate * dt, 0.0)
            b = max(b + net_rate * dt, 0.0)

    return pd.DataFrame(rows)


def vant_hoff_fit(data: pd.DataFrame) -> pd.DataFrame:
    """Fit ln K versus 1/T for each reaction."""
    rows = []

    for reaction, group in data.groupby("reaction"):
        group = group.copy()
        group["inverse_temperature_K_inv"] = 1.0 / group["temperature_K"]
        group["ln_K"] = np.log(group["K"])

        slope, intercept = np.polyfit(group["inverse_temperature_K_inv"], group["ln_K"], deg=1)

        rows.append(
            {
                "reaction": reaction,
                "slope": float(slope),
                "intercept": float(intercept),
                "estimated_delta_h_kj_mol": float((-slope * R_J_MOL_K) / 1000.0),
                "estimated_delta_s_j_mol_k": float(intercept * R_J_MOL_K),
            }
        )

    return pd.DataFrame(rows)


def solubility_product_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """Compare ion product to Ksp."""
    result = data.copy()
    result["ion_product"] = (
        result["cation_concentration_mol_l"] ** result["cation_power"]
        * result["anion_concentration_mol_l"] ** result["anion_power"]
    )
    result["ion_product_over_Ksp"] = result["ion_product"] / result["Ksp"]

    def state(row: pd.Series) -> str:
        if row["ion_product"] > row["Ksp"]:
            return "supersaturated or precipitation favored"
        if row["ion_product"] < row["Ksp"]:
            return "undersaturated or dissolution favored"
        return "at saturation equilibrium"

    result["interpretation"] = result.apply(state, axis=1)
    return result


def activity_scaffold(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simplified activities from concentration and activity coefficient."""
    result = data.copy()
    result["activity"] = (
        result["activity_coefficient"]
        * result["concentration_mol_l"]
        / result["standard_concentration_mol_l"]
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
