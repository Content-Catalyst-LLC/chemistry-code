"""
Core utilities for inorganic chemistry and non-carbon-centered systems.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def oxidation_state_table(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate unknown oxidation states from charge balance."""
    result = data.copy()
    result["unknown_oxidation_state"] = (
        result["total_charge"] - result["known_contribution"]
    ) / result["unknown_atom_count"]
    result["charge_balance_check"] = (
        result["known_contribution"]
        + result["unknown_atom_count"] * result["unknown_oxidation_state"]
    )
    return result


def coordination_summary(complexes: pd.DataFrame) -> pd.DataFrame:
    """Summarize coordination-complex descriptors."""
    result = complexes.copy()
    result["high_coordination"] = (result["coordination_number"] >= 6).astype(int)
    result["low_coordination"] = (result["coordination_number"] <= 2).astype(int)
    result["geometry_family"] = result["geometry"].str.replace("_", " ", regex=False)
    return result


def ligand_summary(ligands: pd.DataFrame) -> pd.DataFrame:
    """Summarize ligand descriptors."""
    result = ligands.copy()
    result["anionic_ligand"] = (result["charge"] < 0).astype(int)
    result["neutral_ligand"] = (result["charge"] == 0).astype(int)
    result["chelating_ligand"] = (result["denticity"] > 1).astype(int)
    return result


def crystal_field_magnetism(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simplified octahedral CFSE and spin-only magnetic moments."""
    result = data.copy()
    result["CFSE_delta_o_units"] = (
        result["t2g_electrons"] * -0.4 * result["delta_o_units"]
        + result["eg_electrons"] * 0.6 * result["delta_o_units"]
    )
    result["spin_only_magnetic_moment_BM"] = result["unpaired_electrons"].apply(
        lambda n: math.sqrt(n * (n + 2))
    )
    result["diamagnetic_hint"] = (result["unpaired_electrons"] == 0).astype(int)
    return result


def ionic_solid_descriptors(data: pd.DataFrame) -> pd.DataFrame:
    """Generate simplified ionic-solid descriptor table."""
    result = data.copy()
    result["charge_product_abs"] = (result["cation_charge"] * result["anion_charge"]).abs()
    result["lattice_energy_relative_scale"] = (
        result["charge_product_abs"] / result["ionic_separation_relative"]
    )
    return result


def perovskite_tolerance(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Goldschmidt tolerance factor for ABX3-like scaffold."""
    result = data.copy()
    result["tolerance_factor"] = (
        (result["r_A"] + result["r_X"])
        / (math.sqrt(2.0) * (result["r_B"] + result["r_X"]))
    )
    result["near_cubic_hint"] = (
        (result["tolerance_factor"] >= 0.9) & (result["tolerance_factor"] <= 1.05)
    ).astype(int)
    return result


def material_descriptor_table(data: pd.DataFrame) -> pd.DataFrame:
    """Generate simplified inorganic materials descriptor scores."""
    result = data.copy()
    result["elemental_diversity_score"] = result["metal_count"] + result["nonmetal_count"]
    result["oxide_rich_hint"] = (result["oxygen_count"] >= 3).astype(int)
    result["redox_active_material_hint"] = (
        (result["transition_metal_present"] == 1)
        & (result["formal_average_metal_oxidation_state"] >= 2)
    ).astype(int)
    result["solid_material_hint"] = (
        result["structure_dimensionality_hint"].str.contains("solid", case=False, regex=False)
    ).astype(int)
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
