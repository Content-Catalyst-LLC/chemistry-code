"""
Core utilities for cheminformatics and molecular data science workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def descriptor_table(descriptors: pd.DataFrame) -> pd.DataFrame:
    """Calculate descriptor scaffolds."""
    result = descriptors.copy()
    result["hetero_atom_fraction"] = result["hetero_atoms"] / result["heavy_atoms"]
    result["polarity_score"] = result["h_bond_donors"] + result["h_bond_acceptors"]
    result["flexibility_score"] = result["rotatable_bonds"] / result["heavy_atoms"]
    result["ring_density"] = result["rings"] / result["heavy_atoms"]
    return result


def graph_table(graphs: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple molecular graph descriptors."""
    result = graphs.copy()
    result["average_degree"] = np.where(
        result["node_count"] > 0,
        2 * result["edge_count"] / result["node_count"],
        0.0,
    )
    result["aromatic_edge_fraction"] = np.where(
        result["edge_count"] > 0,
        result["aromatic_edges"] / result["edge_count"],
        0.0,
    )
    return result


def merge_molecule_descriptors(molecules: pd.DataFrame, descriptors: pd.DataFrame, graphs: pd.DataFrame) -> pd.DataFrame:
    """Join molecule metadata with descriptor and graph tables."""
    return (
        molecules.merge(descriptor_table(descriptors), on="molecule_id", how="left")
        .merge(graph_table(graphs), on="molecule_id", how="left")
    )


def pairwise_tanimoto(fingerprints: pd.DataFrame) -> pd.DataFrame:
    """Calculate pairwise Tanimoto similarity for binary fingerprints."""
    bit_cols = [col for col in fingerprints.columns if col.startswith("bit_")]
    rows = []

    for i in range(len(fingerprints)):
        for j in range(i + 1, len(fingerprints)):
            row_a = fingerprints.iloc[i]
            row_b = fingerprints.iloc[j]

            a_bits = row_a[bit_cols].to_numpy(dtype=int)
            b_bits = row_b[bit_cols].to_numpy(dtype=int)

            a = int(np.sum(a_bits == 1))
            b = int(np.sum(b_bits == 1))
            c = int(np.sum((a_bits == 1) & (b_bits == 1)))

            tanimoto = c / (a + b - c) if (a + b - c) else 0.0

            rows.append(
                {
                    "molecule_a": row_a["molecule_id"],
                    "molecule_b": row_b["molecule_id"],
                    "features_a": a,
                    "features_b": b,
                    "shared_features": c,
                    "tanimoto": tanimoto,
                }
            )

    return pd.DataFrame(rows)


def assay_standardization(assays: pd.DataFrame) -> pd.DataFrame:
    """Standardize nM assay values to molar values and pIC50-like values."""
    result = assays.copy()
    result["value_M"] = np.where(
        result["unit"].str.lower() == "nm",
        result["value"] * 1e-9,
        np.nan,
    )
    result["p_activity"] = -np.log10(result["value_M"])
    result["standardization_warning"] = np.where(
        result["relation"] == "=",
        "exact_value_used",
        "non_exact_relation_requires_caution",
    )
    return result


def scaffold_split_summary(split_data: pd.DataFrame) -> pd.DataFrame:
    """Summarize scaffold split membership."""
    return (
        split_data.groupby(["split", "scaffold"])
        .size()
        .reset_index(name="molecule_count")
        .sort_values(["split", "scaffold"])
    )


def simple_property_model(descriptors: pd.DataFrame, properties: pd.DataFrame) -> pd.DataFrame:
    """Generate a simple transparent linear property scaffold."""
    merged = descriptor_table(descriptors).merge(properties, on="molecule_id", how="inner")
    merged["predicted_value"] = (
        0.15
        + 0.55 * merged["hetero_atom_fraction"]
        + 0.10 * merged["polarity_score"]
        - 0.08 * merged["rings"]
        + 0.05 * merged["flexibility_score"]
    )
    merged["residual"] = merged["value"] - merged["predicted_value"]
    return merged


def applicability_domain(descriptors: pd.DataFrame, splits: pd.DataFrame, queries: pd.DataFrame) -> pd.DataFrame:
    """Calculate nearest-neighbor distance from queries to training descriptor space."""
    desc = descriptor_table(descriptors).merge(splits[["molecule_id", "split"]], on="molecule_id", how="inner")
    train = desc[desc["split"] == "train"].copy()

    feature_cols = [
        "heavy_atoms",
        "hetero_atoms",
        "rings",
        "h_bond_donors",
        "h_bond_acceptors",
        "rotatable_bonds",
    ]

    rows = []
    train_matrix = train[feature_cols].to_numpy(dtype=float)

    for _, query in queries.iterrows():
        q = query[feature_cols].to_numpy(dtype=float)
        distances = np.sqrt(np.sum((train_matrix - q) ** 2, axis=1))
        nearest_index = int(np.argmin(distances))

        rows.append(
            {
                "query_id": query["query_id"],
                "nearest_training_molecule": train.iloc[nearest_index]["molecule_id"],
                "nearest_training_distance": float(distances[nearest_index]),
                "outside_simple_domain_hint": int(distances[nearest_index] > 5.0),
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
