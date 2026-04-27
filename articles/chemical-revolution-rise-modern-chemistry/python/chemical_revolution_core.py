"""
Core utilities for Chemical Revolution workflows.

All examples are synthetic and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib

import pandas as pd


def check_mass_conservation(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate mass difference and conservation flag."""
    result = data.copy()
    result["mass_difference_g"] = result["product_mass_g"] - result["reactant_mass_g"]
    result["conserved_exactly"] = result["mass_difference_g"].abs() < 1e-9
    return result


def calculate_oxidation_mass_gain(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate oxide mass and oxygen mass fraction."""
    result = data.copy()
    result["oxide_mass_g"] = result["metal_mass_g"] + result["oxygen_mass_g"]
    result["oxygen_mass_fraction"] = result["oxygen_mass_g"] / result["oxide_mass_g"]
    result["mass_gain_percent"] = 100.0 * result["oxygen_mass_g"] / result["metal_mass_g"]
    return result


def calculate_combustion_stoichiometry(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simplified carbon combustion masses using C + O2 -> CO2."""
    result = data.copy()
    molar_mass_c = 12.011
    molar_mass_o2 = 31.998
    molar_mass_co2 = 44.009

    result["carbon_mass_g"] = result["carbon_moles"] * molar_mass_c
    result["oxygen_mass_required_g"] = result["oxygen_moles_required"] * molar_mass_o2
    result["carbon_dioxide_mass_g"] = result["carbon_dioxide_moles_produced"] * molar_mass_co2
    result["mass_balance_difference_g"] = (
        result["carbon_dioxide_mass_g"]
        - result["carbon_mass_g"]
        - result["oxygen_mass_required_g"]
    )
    return result


def organize_nomenclature(data: pd.DataFrame) -> pd.DataFrame:
    """Sort historical nomenclature mapping."""
    return data.sort_values(["conceptual_shift", "older_name"]).reset_index(drop=True)


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
