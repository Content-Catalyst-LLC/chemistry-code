"""
Core utilities for measurement and quantification workflows.

All examples are synthetic and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def calculate_mass_volume_concentration(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate moles and molarity from mass, molar mass, and volume."""
    result = data.copy()
    result["moles"] = result["mass_g"] / result["molar_mass_g_mol"]
    result["concentration_mol_l"] = result["moles"] / result["volume_l"]
    return result


def fit_linear_calibration(calibration: pd.DataFrame) -> tuple[float, float]:
    """Fit response = slope * concentration + intercept."""
    x = calibration["concentration_mol_l"].to_numpy()
    y = calibration["instrument_response"].to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    return float(slope), float(intercept)


def estimate_unknowns(unknowns: pd.DataFrame, slope: float, intercept: float) -> pd.DataFrame:
    """Estimate unknown concentrations from linear calibration."""
    result = unknowns.copy()
    result["estimated_concentration_mol_l"] = (
        result["instrument_response"] - intercept
    ) / slope
    return result


def summarize_replicates(data: pd.DataFrame, coverage_factor: float = 2.0) -> pd.DataFrame:
    """Calculate mean, standard deviation, RSD, and expanded uncertainty."""
    grouped = data.groupby("sample")["measured_mass_g"]
    result = grouped.agg(["count", "mean", "std"]).reset_index()
    result = result.rename(
        columns={
            "count": "n_replicates",
            "mean": "mean_mass_g",
            "std": "standard_deviation_g",
        }
    )
    result["rsd_percent"] = 100.0 * result["standard_deviation_g"] / result["mean_mass_g"]
    result["standard_uncertainty_g"] = result["standard_deviation_g"] / np.sqrt(result["n_replicates"])
    result["coverage_factor_k"] = coverage_factor
    result["expanded_uncertainty_g"] = coverage_factor * result["standard_uncertainty_g"]
    return result


def calculate_dilution_plan(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate stock volume required using C1V1 = C2V2."""
    result = data.copy()
    result["stock_volume_ml"] = (
        result["target_concentration_mol_l"] * result["final_volume_ml"]
    ) / result["stock_concentration_mol_l"]
    result["diluent_volume_ml"] = result["final_volume_ml"] - result["stock_volume_ml"]
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
