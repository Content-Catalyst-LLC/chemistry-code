"""
Core utilities for atoms, elements, isotopes, and periodic organization.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


AVOGADRO_CONSTANT = 6.02214076e23


def summarize_element_features(elements: pd.DataFrame) -> pd.DataFrame:
    """Summarize element counts by period, block, and category."""
    return (
        elements.groupby(["period", "block", "category"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["period", "block", "category"])
    )


def add_atomic_identity_fields(isotopes: pd.DataFrame) -> pd.DataFrame:
    """Calculate neutron number and neutral electron count for isotopes."""
    result = isotopes.copy()
    result["neutron_number"] = result["mass_number"] - result["atomic_number"]
    result["neutral_electron_count"] = result["atomic_number"]
    return result


def calculate_isotope_weighted_masses(isotopes: pd.DataFrame) -> pd.DataFrame:
    """Calculate isotope-weighted atomic mass by element."""
    enriched = add_atomic_identity_fields(isotopes)
    enriched["weighted_contribution_u"] = (
        enriched["isotopic_mass_u"] * enriched["fractional_abundance"]
    )
    summary = (
        enriched.groupby("element_symbol", as_index=False)
        .agg(
            weighted_atomic_mass_u=("weighted_contribution_u", "sum"),
            abundance_sum=("fractional_abundance", "sum"),
            isotope_count=("isotope", "count"),
        )
        .sort_values("element_symbol")
    )
    return summary


def calculate_periodic_trends(elements: pd.DataFrame) -> pd.DataFrame:
    """Create a compact trend table and simple fitted values for period 2."""
    numeric = elements.copy()
    numeric["electronegativity_pauling"] = pd.to_numeric(
        numeric["electronegativity_pauling"], errors="coerce"
    )

    period_two = numeric[numeric["period"] == 2].dropna(
        subset=["atomic_radius_pm", "first_ionization_kj_mol"]
    )

    radius_slope = np.polyfit(
        period_two["atomic_number"], period_two["atomic_radius_pm"], deg=1
    )
    ionization_slope = np.polyfit(
        period_two["atomic_number"], period_two["first_ionization_kj_mol"], deg=1
    )

    return pd.DataFrame(
        [
            {
                "trend": "period_2_atomic_radius_vs_atomic_number",
                "slope": float(radius_slope[0]),
                "intercept": float(radius_slope[1]),
                "interpretation": "negative slope reflects decreasing radius across period 2 in this simplified dataset",
            },
            {
                "trend": "period_2_ionization_energy_vs_atomic_number",
                "slope": float(ionization_slope[0]),
                "intercept": float(ionization_slope[1]),
                "interpretation": "positive slope reflects generally increasing ionization energy across period 2 in this simplified dataset",
            },
        ]
    )


def calculate_mole_examples(mole_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate moles and estimated entity counts from mass and molar mass."""
    result = mole_data.copy()
    result["amount_mol"] = result["mass_g"] / result["molar_mass_g_mol"]
    result["estimated_entities"] = result["amount_mol"] * AVOGADRO_CONSTANT
    return result


def calculate_percent_composition(compounds: pd.DataFrame) -> pd.DataFrame:
    """Calculate percent composition for formula rows."""
    result = compounds.copy()
    result["element_mass_contribution"] = (
        result["atom_count"] * result["atomic_mass_u"]
    )
    totals = (
        result.groupby("compound", as_index=False)["element_mass_contribution"]
        .sum()
        .rename(columns={"element_mass_contribution": "compound_molar_mass"})
    )
    merged = result.merge(totals, on="compound", how="left")
    merged["percent_by_mass"] = (
        merged["element_mass_contribution"] / merged["compound_molar_mass"] * 100.0
    )
    return merged.sort_values(["compound", "element_symbol"])


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
