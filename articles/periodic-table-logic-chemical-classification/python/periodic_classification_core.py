"""
Core utilities for periodic-table classification workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib

import numpy as np
import pandas as pd


def summarize_classification(elements: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Summarize element classifications by different periodic layers."""
    by_block = (
        elements.groupby("block")
        .size()
        .reset_index(name="count")
        .sort_values("block")
    )
    by_category = (
        elements.groupby("category")
        .size()
        .reset_index(name="count")
        .sort_values(["count", "category"], ascending=[False, True])
    )
    by_family = (
        elements.groupby("family")
        .size()
        .reset_index(name="count")
        .sort_values(["count", "family"], ascending=[False, True])
    )
    by_period_block = (
        elements.groupby(["period", "block"])
        .size()
        .reset_index(name="count")
        .sort_values(["period", "block"])
    )

    return {
        "by_block": by_block,
        "by_category": by_category,
        "by_family": by_family,
        "by_period_block": by_period_block,
    }


def calculate_periodic_trends(elements: pd.DataFrame) -> pd.DataFrame:
    """Fit simple trend lines for radius and ionization energy by period."""
    rows = []

    for period, group in elements.groupby("period"):
        if len(group) < 4:
            continue

        group = group.dropna(subset=["atomic_number", "atomic_radius_pm", "first_ionization_kj_mol"])
        if len(group) < 4:
            continue

        radius_fit = np.polyfit(group["atomic_number"], group["atomic_radius_pm"], deg=1)
        ion_fit = np.polyfit(group["atomic_number"], group["first_ionization_kj_mol"], deg=1)

        rows.append(
            {
                "period": int(period),
                "trend": "atomic_radius_vs_atomic_number",
                "slope": float(radius_fit[0]),
                "intercept": float(radius_fit[1]),
            }
        )
        rows.append(
            {
                "period": int(period),
                "trend": "first_ionization_vs_atomic_number",
                "slope": float(ion_fit[0]),
                "intercept": float(ion_fit[1]),
            }
        )

    return pd.DataFrame(rows)


def compute_element_similarity(elements: pd.DataFrame) -> pd.DataFrame:
    """Compute simplified element similarity from selected standardized features."""
    feature_columns = [
        "group",
        "period",
        "atomic_radius_pm",
        "first_ionization_kj_mol",
        "electronegativity_pauling",
    ]

    data = elements.dropna(subset=feature_columns).reset_index(drop=True)
    features = data[feature_columns].astype(float)
    scaled = (features - features.mean()) / features.std(ddof=0)

    rows = []
    for i, row_i in data.iterrows():
        for j, row_j in data.iterrows():
            if j <= i:
                continue
            distance = float(np.linalg.norm(scaled.iloc[i] - scaled.iloc[j]))
            rows.append(
                {
                    "element_a": row_i["symbol"],
                    "element_b": row_j["symbol"],
                    "family_a": row_i["family"],
                    "family_b": row_j["family"],
                    "feature_distance": distance,
                }
            )

    return pd.DataFrame(rows).sort_values("feature_distance")


def isotope_weighted_masses(isotopes: pd.DataFrame) -> pd.DataFrame:
    """Calculate isotope-weighted atomic masses from simplified isotope table."""
    result = isotopes.copy()
    result["neutron_number"] = result["mass_number"] - result["atomic_number"]
    result["weighted_contribution_u"] = (
        result["isotopic_mass_u"] * result["fractional_abundance"]
    )

    return (
        result.groupby("element_symbol", as_index=False)
        .agg(
            isotope_count=("isotope", "count"),
            abundance_sum=("fractional_abundance", "sum"),
            weighted_atomic_mass_u=("weighted_contribution_u", "sum"),
        )
        .sort_values("element_symbol")
    )


def build_feature_matrix(elements: pd.DataFrame) -> pd.DataFrame:
    """Build a compact feature matrix for periodic classification."""
    block_map = {"s": 1, "p": 2, "d": 3, "f": 4}
    result = elements.copy()
    result["block_code"] = result["block"].map(block_map)
    return result[
        [
            "symbol",
            "atomic_number",
            "group",
            "period",
            "block",
            "block_code",
            "category",
            "family",
            "atomic_radius_pm",
            "first_ionization_kj_mol",
            "electronegativity_pauling",
        ]
    ]


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
