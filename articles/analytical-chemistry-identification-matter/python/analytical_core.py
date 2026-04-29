"""
Core utilities for analytical chemistry workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def linear_calibration(standards: pd.DataFrame) -> dict[str, float]:
    """Fit a simple unweighted linear calibration model."""
    x = standards["concentration_mg_L"].to_numpy(dtype=float)
    y = standards["signal"].to_numpy(dtype=float)

    slope, intercept = np.polyfit(x, y, deg=1)
    predicted = slope * x + intercept

    ss_res = float(np.sum((y - predicted) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
    }


def calibration_lod_loq(
    standards: pd.DataFrame,
    blanks: pd.DataFrame,
    unknowns: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate calibration model, blank statistics, LOD, LOQ, and unknown concentrations."""
    model = linear_calibration(standards)
    blank_mean = float(blanks["signal"].mean())
    blank_sd = float(blanks["signal"].std(ddof=1))

    lod = 3.0 * blank_sd / model["slope"]
    loq = 10.0 * blank_sd / model["slope"]

    model_table = pd.DataFrame(
        [
            {
                **model,
                "blank_mean": blank_mean,
                "blank_sd": blank_sd,
                "LOD_mg_L": lod,
                "LOQ_mg_L": loq,
            }
        ]
    )

    result = unknowns.copy()
    result["estimated_concentration_mg_L"] = (
        (result["signal"] - model["intercept"]) / model["slope"]
    ) * result["dilution_factor"]
    result["above_LOD"] = (result["estimated_concentration_mg_L"] >= lod).astype(int)
    result["above_LOQ"] = (result["estimated_concentration_mg_L"] >= loq).astype(int)

    return model_table, result


def replicate_precision(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate mean, SD, and RSD for replicate measurements."""
    rows = []

    for sample_id, group in data.groupby("sample_id"):
        mean_value = float(group["measured_mg_L"].mean())
        sd_value = float(group["measured_mg_L"].std(ddof=1))
        rsd_percent = 100.0 * sd_value / mean_value if mean_value != 0 else float("nan")

        rows.append(
            {
                "sample_id": sample_id,
                "n": len(group),
                "mean_mg_L": mean_value,
                "sd_mg_L": sd_value,
                "RSD_percent": rsd_percent,
            }
        )

    return pd.DataFrame(rows)


def spike_recovery(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate spike recovery percentages."""
    result = data.copy()
    result["recovery_percent"] = 100.0 * (
        result["spiked_mg_L"] - result["unspiked_mg_L"]
    ) / result["spike_added_mg_L"]
    result["within_80_120_percent"] = (
        (result["recovery_percent"] >= 80.0) & (result["recovery_percent"] <= 120.0)
    ).astype(int)
    return result


def chromatographic_resolution(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate chromatographic resolution for peak pairs."""
    result = data.copy()
    result["resolution"] = 2.0 * (result["tR_2_min"] - result["tR_1_min"]) / (
        result["w1_min"] + result["w2_min"]
    )
    result["baseline_separation_hint"] = (result["resolution"] >= 1.5).astype(int)
    return result


def beer_lambert_quantification(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate concentration from Beer-Lambert law."""
    result = data.copy()
    result["concentration_mol_L"] = result["absorbance"] / (
        result["epsilon_L_mol_cm"] * result["path_length_cm"]
    )
    return result


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denominator == 0.0:
        return float("nan")
    return float(np.dot(a, b) / denominator)


def spectral_similarity(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple spectral similarity of unknown X to reference spectra."""
    unknown = data["unknown_X"].to_numpy(dtype=float)

    rows = []
    for reference_col in ["reference_A", "reference_B"]:
        ref = data[reference_col].to_numpy(dtype=float)
        rows.append(
            {
                "unknown": "unknown_X",
                "reference": reference_col,
                "cosine_similarity": cosine_similarity(unknown, ref),
                "euclidean_distance": float(np.linalg.norm(unknown - ref)),
            }
        )

    result = pd.DataFrame(rows)
    result["best_match_hint"] = (
        result["cosine_similarity"] == result["cosine_similarity"].max()
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
