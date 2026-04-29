"""
Core utilities for biochemistry workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math
from collections import Counter

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618


def michaelis_menten(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Michaelis-Menten velocities."""
    result = data.copy()
    result["velocity_units"] = (
        result["Vmax_units"] * result["substrate_mM"] / (result["Km_mM"] + result["substrate_mM"])
    )
    result["fraction_of_Vmax"] = result["velocity_units"] / result["Vmax_units"]
    return result


def binding_occupancy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple and Hill-type fractional occupancy."""
    result = data.copy()
    result["simple_fractional_occupancy"] = result["ligand_uM"] / (
        result["Kd_uM"] + result["ligand_uM"]
    )
    result["hill_fractional_occupancy"] = (
        result["ligand_uM"] ** result["hill_n"]
    ) / (
        result["Kd_uM"] ** result["hill_n"] + result["ligand_uM"] ** result["hill_n"]
    )
    return result


def sequence_composition_table(sequences: pd.DataFrame) -> pd.DataFrame:
    """Calculate residue or nucleotide composition."""
    rows = []

    for _, row in sequences.iterrows():
        sequence = str(row["sequence"]).strip().upper()
        counts = Counter(sequence)
        total = len(sequence)

        for symbol, count in sorted(counts.items()):
            rows.append(
                {
                    "sequence_id": row["sequence_id"],
                    "sequence_type": row["sequence_type"],
                    "symbol": symbol,
                    "count": count,
                    "fraction": count / total if total else 0.0,
                    "sequence_length": total,
                }
            )

    return pd.DataFrame(rows)


def biomolecule_class_descriptors(data: pd.DataFrame) -> pd.DataFrame:
    """Generate simple biomolecule class descriptors."""
    result = data.copy()
    result["is_polymer"] = result["polymer_or_assembly"].str.contains("polymer", case=False, regex=False).astype(int)
    result["is_assembly"] = result["polymer_or_assembly"].str.contains("assembly", case=False, regex=False).astype(int)
    result["function_token_count"] = result["major_functions"].str.split("_").apply(len)
    return result


def flux_balance(stoich: pd.DataFrame, flux_cases: pd.DataFrame) -> pd.DataFrame:
    """Calculate S v balance for simplified metabolic flux cases."""
    metabolites = stoich["metabolite"].tolist()
    reaction_cols = [col for col in stoich.columns if col != "metabolite"]
    S = stoich[reaction_cols].to_numpy(dtype=float)

    rows = []
    for _, case in flux_cases.iterrows():
        v = case[reaction_cols].to_numpy(dtype=float)
        balance = S @ v

        for metabolite, value in zip(metabolites, balance):
            rows.append(
                {
                    "case_id": case["case_id"],
                    "metabolite": metabolite,
                    "balance": value,
                    "steady_state_hint": int(abs(value) < 1.0e-9),
                }
            )

    return pd.DataFrame(rows)


def network_summary(edges: pd.DataFrame) -> pd.DataFrame:
    """Summarize a simplified biochemical interaction network."""
    nodes = sorted(set(edges["source"]).union(set(edges["target"])))
    degree = {node: 0 for node in nodes}

    for _, edge in edges.iterrows():
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    return pd.DataFrame(
        {
            "node": list(degree.keys()),
            "degree": list(degree.values()),
        }
    ).sort_values("degree", ascending=False)


def biochemical_free_energy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate standard free energy from equilibrium constants."""
    result = data.copy()
    result["delta_g_standard_kj_mol"] = result.apply(
        lambda row: -(R_J_MOL_K * row["temperature_K"] * math.log(row["equilibrium_constant"])) / 1000.0,
        axis=1,
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
