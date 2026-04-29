"""
Core utilities for chemical biology workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib

import numpy as np
import pandas as pd


def dose_response(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate a simple four-parameter-style dose-response scaffold."""
    result = data.copy()
    result["response_fraction"] = result["bottom"] + (result["top"] - result["bottom"]) / (
        1.0 + (result["EC50_uM"] / result["compound_uM"]) ** result["hill_slope"]
    )
    return result


def occupancy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate fractional target occupancy."""
    result = data.copy()
    result["fractional_occupancy"] = result["ligand_uM"] / (
        result["Kd_uM"] + result["ligand_uM"]
    )
    return result


def target_engagement(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate target engagement fraction from assay signals."""
    result = data.copy()
    result["target_engagement_fraction"] = (
        result["signal_control"] - result["signal_treated"]
    ) / (
        result["signal_control"] - result["signal_max"]
    )
    result["target_engagement_fraction"] = result["target_engagement_fraction"].clip(lower=0, upper=1)
    return result


def probe_quality(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate a simple educational probe quality score."""
    result = data.copy()
    result["selectivity_ratio"] = result["off_target_potency_nM"] / result["target_potency_nM"]
    result["quality_score"] = (
        (result["selectivity_ratio"].clip(upper=100.0) / 100.0)
        + result["cellular_target_engagement"]
        + 0.25 * result["inactive_control_available"]
        + 0.10 * result["solubility_flag"]
        + 0.10 * result["viability_flag"]
    )
    result["strong_probe_hint"] = (
        (result["selectivity_ratio"] >= 30)
        & (result["cellular_target_engagement"] >= 0.75)
        & (result["inactive_control_available"] == 1)
        & (result["viability_flag"] == 1)
    ).astype(int)
    return result


def chemoproteomics_competition(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate apparent target engagement from competition-like intensity data."""
    result = data.copy()
    result["treated_depletion_fraction"] = (
        result["control_intensity"] - result["treated_intensity"]
    ) / result["control_intensity"]
    result["competition_rescue_fraction"] = (
        result["competition_intensity"] - result["treated_intensity"]
    ) / (
        result["control_intensity"] - result["treated_intensity"]
    )
    result["competition_rescue_fraction"] = result["competition_rescue_fraction"].clip(lower=0, upper=1)
    result["candidate_specific_target_hint"] = (
        (result["treated_depletion_fraction"] >= 0.40)
        & (result["competition_rescue_fraction"] >= 0.50)
    ).astype(int)
    return result


def selectivity_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize compound selectivity against listed off-targets."""
    rows = []
    for compound, group in data.groupby("compound"):
        primary = group[group["target_class"] == "primary"]["activity_nM"].min()
        off_target = group[group["target_class"] == "off_target"]["activity_nM"].min()
        ratio = off_target / primary if primary > 0 else np.nan
        rows.append(
            {
                "compound": compound,
                "primary_activity_nM": primary,
                "best_off_target_activity_nM": off_target,
                "selectivity_ratio": ratio,
                "selective_hint": int(ratio >= 30),
            }
        )
    return pd.DataFrame(rows)


def perturbation_vector(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple perturbation vector from treated-control features."""
    result = data.copy()
    result["delta"] = result["treated"] - result["control"]
    result["absolute_delta"] = result["delta"].abs()
    result["direction"] = np.where(result["delta"] >= 0, "increased", "decreased")
    return result.sort_values("absolute_delta", ascending=False)


def network_summary(edges: pd.DataFrame) -> pd.DataFrame:
    """Summarize a chemical-biology perturbation network."""
    nodes = sorted(set(edges["source"]).union(set(edges["target"])))
    degree = {node: 0 for node in nodes}
    signed_weight = {node: 0.0 for node in nodes}

    for _, edge in edges.iterrows():
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1
        signed_weight[edge["source"]] += edge["weight"]
        signed_weight[edge["target"]] += edge["weight"]

    return pd.DataFrame(
        {
            "node": list(degree.keys()),
            "degree": [degree[node] for node in degree],
            "signed_weight_sum": [signed_weight[node] for node in degree],
        }
    ).sort_values(["degree", "signed_weight_sum"], ascending=False)


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
