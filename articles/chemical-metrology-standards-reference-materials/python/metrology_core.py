"""
Core utilities for chemical metrology workflows.

All examples are synthetic and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def summarize_uncertainty_budget(data: pd.DataFrame, coverage_factor: float = 2.0) -> pd.DataFrame:
    """Calculate combined standard uncertainty and expanded uncertainty."""
    combined = math.sqrt(float((data["standard_uncertainty"] ** 2).sum()))
    expanded = coverage_factor * combined
    contribution = data.copy()
    contribution["variance_contribution"] = contribution["standard_uncertainty"] ** 2
    total_variance = contribution["variance_contribution"].sum()
    contribution["percent_variance_contribution"] = (
        100.0 * contribution["variance_contribution"] / total_variance
    )

    summary = pd.DataFrame(
        [
            {
                "combined_standard_uncertainty": combined,
                "coverage_factor_k": coverage_factor,
                "expanded_uncertainty": expanded,
                "unit": data["unit"].iloc[0],
            }
        ]
    )

    return contribution, summary


def summarize_reference_materials(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate relative expanded uncertainty for reference materials."""
    result = data.copy()
    result["relative_expanded_uncertainty_percent"] = (
        100.0 * result["expanded_uncertainty"] / result["certified_value"].abs()
    )
    return result


def summarize_traceability_chain(data: pd.DataFrame) -> pd.DataFrame:
    """Add cumulative uncertainty to a traceability chain using root-sum-square."""
    result = data.copy()
    cumulative = []
    running_variance = 0.0
    for uncertainty in result["expanded_uncertainty"]:
        running_variance += float(uncertainty) ** 2
        cumulative.append(math.sqrt(running_variance))
    result["cumulative_root_sum_square_uncertainty"] = cumulative
    return result


def calculate_interlaboratory_en(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate normalized error for interlaboratory comparison."""
    result = data.copy()
    denominator = np.sqrt(
        result["lab_expanded_uncertainty"] ** 2
        + result["reference_expanded_uncertainty"] ** 2
    )
    result["bias"] = result["lab_result"] - result["reference_value"]
    result["normalized_error_en"] = result["bias"] / denominator
    result["acceptable_by_abs_en_le_1"] = result["normalized_error_en"].abs() <= 1.0
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
