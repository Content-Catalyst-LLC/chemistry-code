"""
Core utilities for chemical kinetics and reaction-mechanism workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618


def fit_first_order(data: pd.DataFrame) -> pd.DataFrame:
    """Fit ln concentration versus time for each first-order experiment."""
    rows = []

    for experiment, group in data.groupby("experiment"):
        group = group.copy()
        group["ln_concentration"] = np.log(group["concentration_mol_l"])

        slope, intercept = np.polyfit(
            group["time_min"],
            group["ln_concentration"],
            deg=1,
        )

        k = -slope
        rows.append(
            {
                "experiment": experiment,
                "rate_constant_per_min": k,
                "initial_concentration_estimate_mol_l": math.exp(intercept),
                "half_life_min": math.log(2) / k,
            }
        )

    return pd.DataFrame(rows)


def integrated_rate_law_trajectories(examples: pd.DataFrame) -> pd.DataFrame:
    """Generate zero-, first-, and second-order trajectories."""
    rows = []

    for _, row in examples.iterrows():
        times = np.arange(0, row["total_time"] + row["time_step"], row["time_step"])
        c0 = row["initial_concentration_mol_l"]
        k = row["rate_constant"]
        order = int(row["order"])

        for t in times:
            if order == 0:
                concentration = max(c0 - k * t, 0.0)
            elif order == 1:
                concentration = c0 * math.exp(-k * t)
            elif order == 2:
                concentration = 1.0 / ((1.0 / c0) + k * t)
            else:
                raise ValueError("Only orders 0, 1, and 2 are supported.")

            rows.append(
                {
                    "case_id": row["case_id"],
                    "order": order,
                    "time": float(t),
                    "concentration_mol_l": concentration,
                }
            )

    return pd.DataFrame(rows)


def arrhenius_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """Estimate activation energy and pre-exponential factor from Arrhenius data."""
    rows = []

    for reaction, group in data.groupby("reaction"):
        group = group.copy()
        group["inverse_temperature_K_inv"] = 1.0 / group["temperature_K"]
        group["ln_k"] = np.log(group["rate_constant_s_inv"])

        slope, intercept = np.polyfit(
            group["inverse_temperature_K_inv"],
            group["ln_k"],
            deg=1,
        )

        rows.append(
            {
                "reaction": reaction,
                "slope": float(slope),
                "intercept": float(intercept),
                "activation_energy_kj_mol": float((-slope * R_J_MOL_K) / 1000.0),
                "pre_exponential_factor_s_inv": float(math.exp(intercept)),
            }
        )

    return pd.DataFrame(rows)


def simulate_consecutive_mechanism(parameters: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate A -> B -> C using transparent Euler integration.

    This intentionally prioritizes clarity over production-grade numerical accuracy.
    """
    rows = []

    for _, row in parameters.iterrows():
        time_values = np.arange(0, row["total_time_min"] + row["time_step_min"], row["time_step_min"])
        dt = row["time_step_min"]

        a = float(row["A0_mol_l"])
        b = float(row["B0_mol_l"])
        c = float(row["C0_mol_l"])

        for t in time_values:
            rows.append(
                {
                    "mechanism": row["mechanism"],
                    "time_min": float(t),
                    "A_mol_l": a,
                    "B_mol_l": b,
                    "C_mol_l": c,
                }
            )

            rate1 = row["k1_per_min"] * a
            rate2 = row["k2_per_min"] * b

            a_next = max(a - rate1 * dt, 0.0)
            b_next = max(b + (rate1 - rate2) * dt, 0.0)
            c_next = max(c + rate2 * dt, 0.0)

            a, b, c = a_next, b_next, c_next

    return pd.DataFrame(rows)


def enzyme_lineweaver_burk(data: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate Michaelis-Menten parameters using a Lineweaver-Burk linearization.

    This is educational. Nonlinear fitting is preferred for serious analysis.
    """
    rows = []

    for experiment, group in data.groupby("experiment"):
        group = group.copy()
        group["inverse_substrate"] = 1.0 / group["substrate_mM"]
        group["inverse_rate"] = 1.0 / group["rate_umol_min"]

        slope, intercept = np.polyfit(
            group["inverse_substrate"],
            group["inverse_rate"],
            deg=1,
        )

        vmax = 1.0 / intercept
        km = slope * vmax

        rows.append(
            {
                "experiment": experiment,
                "vmax_umol_min": float(vmax),
                "km_mM": float(km),
                "method": "Lineweaver-Burk educational linearization",
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
