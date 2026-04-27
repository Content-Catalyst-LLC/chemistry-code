"""
Core utilities for introductory chemistry workflows.

All examples are synthetic and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import pandas as pd


def add_moles_and_molarity(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate moles and molarity from mass, molar mass, and volume."""
    result = data.copy()
    result["moles"] = result["mass_g"] / result["molar_mass_g_mol"]
    result["molarity_mol_l"] = result["moles"] / result["volume_l"]
    return result


def simulate_first_order(row: pd.Series) -> pd.DataFrame:
    """Simulate first-order concentration decay."""
    rows = []
    total_time = int(row["total_time_min"])
    step = int(row["time_step_min"])
    for time in range(0, total_time + 1, step):
        concentration = float(row["initial_concentration_mol_l"]) * math.exp(
            -float(row["rate_constant_per_min"]) * time
        )
        rows.append(
            {
                "reaction": row["reaction"],
                "time_min": time,
                "concentration_mol_l": concentration,
            }
        )
    return pd.DataFrame(rows)


def beer_lambert_fit(calibration: pd.DataFrame) -> dict:
    """Fit absorbance = slope * concentration + intercept using simple formulas."""
    x = calibration["concentration_mol_l"]
    y = calibration["absorbance"]

    x_mean = x.mean()
    y_mean = y.mean()

    slope = ((x - x_mean) * (y - y_mean)).sum() / ((x - x_mean) ** 2).sum()
    intercept = y_mean - slope * x_mean

    return {"slope": slope, "intercept": intercept}


def calculate_ph(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simplified pH from hydrogen ion concentration."""
    result = data.copy()
    result["pH"] = -result["hydrogen_concentration_mol_l"].apply(math.log10)
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
