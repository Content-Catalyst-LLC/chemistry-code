"""
Core utilities for acid-base chemistry and proton-transfer workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


KW_25C = 1.0e-14


def weak_acid_ph(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate weak acid pH using the exact quadratic solution for HA."""
    rows = []

    for _, row in data.iterrows():
        ka = float(row["Ka"])
        c = float(row["initial_concentration_mol_l"])

        h = (-ka + math.sqrt(ka * ka + 4.0 * ka * c)) / 2.0
        ph = -math.log10(h)
        percent_dissociation = h / c * 100.0

        rows.append(
            {
                "case_id": row["case_id"],
                "species": row["acid"],
                "type": "weak_acid",
                "equilibrium_constant": ka,
                "initial_concentration_mol_l": c,
                "hydronium_mol_l": h,
                "hydroxide_mol_l": KW_25C / h,
                "pH": ph,
                "pOH": 14.0 - ph,
                "percent_dissociation": percent_dissociation,
            }
        )

    return pd.DataFrame(rows)


def weak_base_ph(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate weak base pH using the exact quadratic solution for B."""
    rows = []

    for _, row in data.iterrows():
        kb = float(row["Kb"])
        c = float(row["initial_concentration_mol_l"])

        oh = (-kb + math.sqrt(kb * kb + 4.0 * kb * c)) / 2.0
        poh = -math.log10(oh)
        ph = 14.0 - poh
        percent_protonation = oh / c * 100.0

        rows.append(
            {
                "case_id": row["case_id"],
                "species": row["base"],
                "type": "weak_base",
                "equilibrium_constant": kb,
                "initial_concentration_mol_l": c,
                "hydronium_mol_l": KW_25C / oh,
                "hydroxide_mol_l": oh,
                "pH": ph,
                "pOH": poh,
                "percent_dissociation": percent_protonation,
            }
        )

    return pd.DataFrame(rows)


def buffer_ph(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate buffer pH using the Henderson-Hasselbalch relationship."""
    result = data.copy()
    result["base_to_acid_ratio"] = result["conjugate_base_mol_l"] / result["weak_acid_mol_l"]
    result["pH"] = result["pKa"] + np.log10(result["base_to_acid_ratio"])
    result["total_buffer_mol_l"] = result["weak_acid_mol_l"] + result["conjugate_base_mol_l"]
    return result


def strong_acid_strong_base_curve(acid_c: float, acid_v: float, base_c: float) -> pd.DataFrame:
    """Generate a strong acid-strong base titration curve scaffold."""
    rows = []
    acid_moles = acid_c * acid_v

    for base_v in np.linspace(0.0, 2.0 * acid_v, 101):
        base_moles = base_c * base_v
        total_volume = acid_v + base_v

        if base_moles < acid_moles:
            h = (acid_moles - base_moles) / total_volume
            ph = -math.log10(h)
        elif base_moles > acid_moles:
            oh = (base_moles - acid_moles) / total_volume
            ph = 14.0 + math.log10(oh)
        else:
            ph = 7.0

        rows.append(
            {
                "titration_type": "strong_acid_strong_base",
                "base_volume_ml": base_v * 1000.0,
                "pH": ph,
            }
        )

    return pd.DataFrame(rows)


def weak_acid_strong_base_curve(acid_c: float, acid_v: float, base_c: float, ka: float) -> pd.DataFrame:
    """
    Generate a weak acid-strong base titration curve scaffold.

    This is a simplified educational model.
    """
    rows = []
    acid_moles = acid_c * acid_v
    pka = -math.log10(ka)
    equivalence_volume = acid_moles / base_c

    for base_v in np.linspace(0.0, 2.0 * equivalence_volume, 101):
        base_moles = base_c * base_v
        total_volume = acid_v + base_v

        if base_v == 0:
            h = (-ka + math.sqrt(ka * ka + 4.0 * ka * acid_c)) / 2.0
            ph = -math.log10(h)
            region = "initial weak acid"
        elif base_moles < acid_moles:
            acid_remaining = acid_moles - base_moles
            conjugate_base = base_moles
            ph = pka + math.log10(conjugate_base / acid_remaining)
            region = "buffer region"
        elif abs(base_moles - acid_moles) < 1e-12:
            kb = KW_25C / ka
            conjugate_base_concentration = acid_moles / total_volume
            oh = (-kb + math.sqrt(kb * kb + 4.0 * kb * conjugate_base_concentration)) / 2.0
            ph = 14.0 + math.log10(oh)
            region = "equivalence"
        else:
            excess_oh = (base_moles - acid_moles) / total_volume
            ph = 14.0 + math.log10(excess_oh)
            region = "excess strong base"

        rows.append(
            {
                "titration_type": "weak_acid_strong_base",
                "base_volume_ml": base_v * 1000.0,
                "pH": ph,
                "region": region,
            }
        )

    return pd.DataFrame(rows)


def titration_curves(data: pd.DataFrame) -> pd.DataFrame:
    """Generate titration curve tables from case definitions."""
    frames = []

    for _, row in data.iterrows():
        if row["titration_type"] == "strong_acid_strong_base":
            curve = strong_acid_strong_base_curve(
                row["acid_concentration_mol_l"],
                row["acid_volume_l"],
                row["base_concentration_mol_l"],
            )
        else:
            curve = weak_acid_strong_base_curve(
                row["acid_concentration_mol_l"],
                row["acid_volume_l"],
                row["base_concentration_mol_l"],
                row["Ka"],
            )

        curve.insert(0, "case_id", row["case_id"])
        frames.append(curve)

    return pd.concat(frames, ignore_index=True)


def monoprotic_speciation(data: pd.DataFrame) -> pd.DataFrame:
    """Generate fraction protonated/deprotonated for monoprotic acids."""
    rows = []

    for _, row in data.iterrows():
        ka = 10.0 ** (-float(row["pKa"]))
        ph_values = np.arange(row["pH_min"], row["pH_max"] + row["pH_step"], row["pH_step"])

        for ph in ph_values:
            h = 10.0 ** (-ph)
            alpha_ha = h / (h + ka)
            alpha_a = ka / (h + ka)

            rows.append(
                {
                    "case_id": row["case_id"],
                    "acid": row["acid"],
                    "pH": float(ph),
                    "alpha_HA": alpha_ha,
                    "alpha_A_minus": alpha_a,
                }
            )

    return pd.DataFrame(rows)


def polyprotic_distribution(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate simplified distribution fractions for diprotic/triprotic acids.

    For triprotic H3A:
    alpha0 = H^3 / D
    alpha1 = Ka1 H^2 / D
    alpha2 = Ka1 Ka2 H / D
    alpha3 = Ka1 Ka2 Ka3 / D

    For diprotic H2A, Ka3 is treated as zero and triprotic alpha3 is zero.
    """
    rows = []

    for _, row in data.iterrows():
        ka1 = 10.0 ** (-float(row["pKa1"]))
        ka2 = 10.0 ** (-float(row["pKa2"]))
        ka3 = 0.0 if pd.isna(row["pKa3"]) else 10.0 ** (-float(row["pKa3"]))

        for ph in np.arange(0.0, 14.5, 0.5):
            h = 10.0 ** (-ph)

            if ka3 > 0:
                denominator = h**3 + ka1 * h**2 + ka1 * ka2 * h + ka1 * ka2 * ka3
                alpha0 = h**3 / denominator
                alpha1 = ka1 * h**2 / denominator
                alpha2 = ka1 * ka2 * h / denominator
                alpha3 = ka1 * ka2 * ka3 / denominator
            else:
                denominator = h**2 + ka1 * h + ka1 * ka2
                alpha0 = h**2 / denominator
                alpha1 = ka1 * h / denominator
                alpha2 = ka1 * ka2 / denominator
                alpha3 = 0.0

            rows.append(
                {
                    "case_id": row["case_id"],
                    "system": row["system"],
                    "pH": float(ph),
                    "alpha_fully_protonated": alpha0,
                    "alpha_once_deprotonated": alpha1,
                    "alpha_twice_deprotonated": alpha2,
                    "alpha_thrice_deprotonated": alpha3,
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
