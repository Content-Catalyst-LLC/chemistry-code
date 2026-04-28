"""
Core utilities for stoichiometry and quantitative reaction workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_L_ATM_MOL_K = 0.082057338
MOLAR_MASS_C = 12.011
MOLAR_MASS_H = 1.008
MOLAR_MASS_O = 15.999
MOLAR_MASS_CO2 = 44.0095
MOLAR_MASS_H2O = 18.01528


def limiting_reagent_and_yield(reactions: pd.DataFrame, examples: pd.DataFrame) -> pd.DataFrame:
    """Calculate limiting reagent, theoretical yield, and percent yield."""
    reaction_lookup = reactions.set_index("reaction_id")
    rows = []

    for _, example in examples.iterrows():
        reaction = reaction_lookup.loc[example["reaction_id"]]

        extent_a = example["available_a_mol"] / reaction["coefficient_a"]

        coefficient_b = float(reaction["coefficient_b"])
        if coefficient_b > 0 and not pd.isna(example["available_b_mol"]):
            extent_b = example["available_b_mol"] / coefficient_b
        else:
            extent_b = math.inf

        if extent_a <= extent_b:
            limiting_reagent = reaction["reactant_a"]
            maximum_extent = extent_a
        else:
            limiting_reagent = reaction["reactant_b"]
            maximum_extent = extent_b

        theoretical_product_mol = maximum_extent * reaction["coefficient_product"]
        theoretical_yield_g = theoretical_product_mol * reaction["product_molar_mass_g_mol"]
        percent_yield = example["actual_yield_g"] / theoretical_yield_g * 100.0

        rows.append(
            {
                "case_id": example["case_id"],
                "reaction_id": example["reaction_id"],
                "limiting_reagent": limiting_reagent,
                "maximum_extent_mol": maximum_extent,
                "theoretical_product_mol": theoretical_product_mol,
                "theoretical_yield_g": theoretical_yield_g,
                "actual_yield_g": example["actual_yield_g"],
                "percent_yield": percent_yield,
            }
        )

    return pd.DataFrame(rows)


def dilution_calculations(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate required stock volume using C1V1 = C2V2."""
    result = data.copy()
    result["stock_volume_l"] = (
        result["target_concentration_mol_l"] * result["target_volume_l"]
    ) / result["stock_concentration_mol_l"]
    result["stock_volume_ml"] = result["stock_volume_l"] * 1000.0
    return result


def titration_calculations(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate analyte concentration from coefficient-aware titration equivalence.

    C_analyte * V_analyte / a = C_titrant * V_titrant / b
    """
    result = data.copy()
    result["analyte_concentration_mol_l"] = (
        result["analyte_coefficient"]
        * result["titrant_concentration_mol_l"]
        * result["titrant_volume_l"]
        / (result["titrant_coefficient"] * result["analyte_volume_l"])
    )
    return result


def gas_stoichiometry(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate gas moles using PV = nRT, then target product moles."""
    result = data.copy()
    result["gas_moles"] = (
        result["pressure_atm"] * result["volume_l"]
    ) / (R_L_ATM_MOL_K * result["temperature_k"])
    result["target_moles"] = (
        result["gas_moles"] * result["coefficient_target"] / result["coefficient_gas"]
    )
    return result


def empirical_formula_ratios(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate empirical formula mole ratios from percent composition."""
    rows = []
    for case_id, group in data.groupby("case_id"):
        group = group.copy()
        group["moles"] = group["percent_mass"] / group["atomic_mass_g_mol"]
        minimum_moles = group["moles"].min()
        group["ratio"] = group["moles"] / minimum_moles
        group["rounded_ratio"] = group["ratio"].round().astype(int)
        rows.append(group)
    return pd.concat(rows, ignore_index=True)


def combustion_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """Infer C/H/O mole ratios from CO2 and H2O combustion products."""
    rows = []

    for _, row in data.iterrows():
        moles_co2 = row["co2_mass_g"] / MOLAR_MASS_CO2
        moles_h2o = row["h2o_mass_g"] / MOLAR_MASS_H2O

        moles_c = moles_co2
        moles_h = 2.0 * moles_h2o

        mass_c = moles_c * MOLAR_MASS_C
        mass_h = moles_h * MOLAR_MASS_H
        mass_o = row["sample_mass_g"] - mass_c - mass_h
        moles_o = max(mass_o / MOLAR_MASS_O, 0.0)

        mole_values = [value for value in [moles_c, moles_h, moles_o] if value > 0]
        minimum = min(mole_values)

        rows.append(
            {
                "case_id": row["case_id"],
                "moles_c": moles_c,
                "moles_h": moles_h,
                "moles_o": moles_o,
                "ratio_c": moles_c / minimum,
                "ratio_h": moles_h / minimum,
                "ratio_o": moles_o / minimum if moles_o > 0 else 0.0,
            }
        )

    return pd.DataFrame(rows)


def reaction_extent_balances(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate final amounts from n_i = n_i0 + nu_i * xi."""
    result = data.copy()
    result["final_mol"] = (
        result["initial_mol"] + result["stoichiometric_number"] * result["extent_mol"]
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
