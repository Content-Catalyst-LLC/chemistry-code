"""
Core utilities for Python-centered chemistry, simulation, and laboratory data workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618


def fit_calibration(standards: pd.DataFrame) -> dict:
    """Fit a simple linear calibration curve."""
    grouped = (
        standards.groupby("concentration_mM", as_index=False)
        .agg(response_mean=("response", "mean"), response_sd=("response", "std"), n=("response", "count"))
        .sort_values("concentration_mM")
    )

    slope, intercept = np.polyfit(grouped["concentration_mM"], grouped["response_mean"], deg=1)
    grouped["predicted_response"] = slope * grouped["concentration_mM"] + intercept
    grouped["residual"] = grouped["response_mean"] - grouped["predicted_response"]

    rmse = float(np.sqrt(np.mean(grouped["residual"] ** 2)))

    return {
        "grouped": grouped,
        "slope": float(slope),
        "intercept": float(intercept),
        "rmse": rmse,
    }


def estimate_unknowns(unknowns: pd.DataFrame, slope: float, intercept: float) -> pd.DataFrame:
    """Estimate unknown concentrations from calibration model."""
    result = unknowns.copy()
    result["estimated_concentration_mM"] = (result["response"] - intercept) / slope

    summary = (
        result.groupby("sample_id", as_index=False)
        .agg(
            concentration_mean_mM=("estimated_concentration_mM", "mean"),
            concentration_sd_mM=("estimated_concentration_mM", "std"),
            n=("estimated_concentration_mM", "count"),
        )
    )
    summary["concentration_se_mM"] = summary["concentration_sd_mM"] / np.sqrt(summary["n"])
    return summary


def first_order_kinetics(data: pd.DataFrame) -> pd.DataFrame:
    """Fit first-order kinetics using ln concentration versus time."""
    result = data.copy()
    result["ln_concentration"] = np.log(result["concentration_mM"])

    slope, intercept = np.polyfit(result["time_s"], result["ln_concentration"], deg=1)
    k = -float(slope)
    half_life = math.log(2.0) / k

    result["predicted_ln_concentration"] = slope * result["time_s"] + intercept
    result["predicted_concentration_mM"] = np.exp(result["predicted_ln_concentration"])
    result["residual_mM"] = result["concentration_mM"] - result["predicted_concentration_mM"]
    result["k_s_inv"] = k
    result["half_life_s"] = half_life

    return result


def arrhenius_transform(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Arrhenius transformed variables."""
    result = data.copy()
    result["inverse_temperature_K_inv"] = 1.0 / result["temperature_K"]
    result["ln_rate_constant"] = np.log(result["rate_constant_s_inv"])

    slope, intercept = np.polyfit(result["inverse_temperature_K_inv"], result["ln_rate_constant"], deg=1)
    result["arrhenius_slope"] = slope
    result["arrhenius_intercept"] = intercept
    result["activation_energy_J_mol_estimate"] = -slope * R_J_MOL_K
    return result


def replicate_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize replicate measurements."""
    summary = (
        data.groupby(["sample_id", "method_id"], as_index=False)
        .agg(
            mean_mM=("measurement_mM", "mean"),
            sd_mM=("measurement_mM", "std"),
            n=("measurement_mM", "count"),
        )
    )
    summary["se_mM"] = summary["sd_mM"] / np.sqrt(summary["n"])
    summary["relative_sd_percent"] = 100.0 * summary["sd_mM"] / summary["mean_mM"]
    return summary


def simulate_first_order(parameters: pd.DataFrame) -> pd.DataFrame:
    """Generate first-order concentration profiles for simple simulation scenarios."""
    rows = []

    for _, row in parameters.iterrows():
        time_points = np.arange(0.0, row["time_end_s"] + row["time_step_s"], row["time_step_s"])
        concentrations = row["initial_concentration_mM"] * np.exp(-row["rate_constant_s_inv"] * time_points)

        for time_s, concentration in zip(time_points, concentrations):
            rows.append(
                {
                    "simulation_id": row["simulation_id"],
                    "time_s": float(time_s),
                    "concentration_mM": float(concentration),
                    "initial_concentration_mM": float(row["initial_concentration_mM"]),
                    "rate_constant_s_inv": float(row["rate_constant_s_inv"]),
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
