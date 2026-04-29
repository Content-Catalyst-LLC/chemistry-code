"""
Core utilities for organic chemistry and carbon-based structure workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


ATOMIC_WEIGHTS = {
    "C": 12.011,
    "H": 1.008,
    "N": 14.007,
    "O": 15.999,
    "S": 32.06,
    "X": 35.45,
}


def formula_descriptors(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate molecular formula descriptors and DBE."""
    result = data.copy()
    result["DBE"] = (
        result["C"]
        - (result["H"] + result["X"]) / 2.0
        + result["N"] / 2.0
        + 1.0
    )
    result["heteroatom_count"] = result["N"] + result["O"] + result["S"] + result["X"]
    result["heavy_atom_count"] = result["C"] + result["N"] + result["O"] + result["S"] + result["X"]
    result["approx_molecular_weight"] = (
        result["C"] * ATOMIC_WEIGHTS["C"]
        + result["H"] * ATOMIC_WEIGHTS["H"]
        + result["N"] * ATOMIC_WEIGHTS["N"]
        + result["O"] * ATOMIC_WEIGHTS["O"]
        + result["S"] * ATOMIC_WEIGHTS["S"]
        + result["X"] * ATOMIC_WEIGHTS["X"]
    )
    return result


def hybridization_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Return carbon hybridization summary with geometry categories."""
    result = data.copy()
    result["geometry_descriptor"] = (
        result["hybridization"]
        + "_"
        + result["approximate_geometry"].str.replace(" ", "_", regex=False)
    )
    return result


def molecular_graph_summary(atoms: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Calculate simplified graph descriptors for each molecular graph."""
    rows = []

    for molecule, atom_group in atoms.groupby("molecule"):
        edge_group = edges[edges["molecule"] == molecule]
        atom_ids = atom_group["atom_id"].tolist()
        atom_index = {atom_id: i for i, atom_id in enumerate(atom_ids)}

        adjacency = np.zeros((len(atom_ids), len(atom_ids)), dtype=float)

        for _, edge in edge_group.iterrows():
            i = atom_index[edge["atom_a"]]
            j = atom_index[edge["atom_b"]]
            adjacency[i, j] = edge["bond_order"]
            adjacency[j, i] = edge["bond_order"]

        degree_values = (adjacency > 0).sum(axis=1)
        bond_order_sum = adjacency.sum() / 2.0

        rows.append(
            {
                "molecule": molecule,
                "atom_count": len(atom_ids),
                "edge_count": len(edge_group),
                "bond_order_sum": bond_order_sum,
                "mean_graph_degree": float(np.mean(degree_values)) if len(degree_values) else 0.0,
                "max_graph_degree": int(np.max(degree_values)) if len(degree_values) else 0,
                "contains_cycle_simplified": int(len(edge_group) >= len(atom_ids)),
            }
        )

    return pd.DataFrame(rows)


def adjacency_matrix_long(atoms: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Create long-form adjacency records for each molecular graph."""
    rows = []

    for molecule, atom_group in atoms.groupby("molecule"):
        atom_ids = atom_group["atom_id"].tolist()
        edge_group = edges[edges["molecule"] == molecule]

        bond_lookup = {}
        for _, edge in edge_group.iterrows():
            key = tuple(sorted([edge["atom_a"], edge["atom_b"]]))
            bond_lookup[key] = edge["bond_order"]

        for atom_a in atom_ids:
            for atom_b in atom_ids:
                key = tuple(sorted([atom_a, atom_b]))
                bond_order = 0.0 if atom_a == atom_b else bond_lookup.get(key, 0.0)
                rows.append(
                    {
                        "molecule": molecule,
                        "atom_a": atom_a,
                        "atom_b": atom_b,
                        "bond_order": bond_order,
                    }
                )

    return pd.DataFrame(rows)


def functional_group_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize functional group flags."""
    result = data.copy()
    group_columns = [col for col in result.columns if col != "molecule"]
    result["functional_group_count"] = result[group_columns].sum(axis=1)
    result["has_polar_group"] = (
        result[["alcohol", "ether", "amine", "aldehyde", "ketone", "carboxylic_acid", "ester", "amide", "nitrile", "thiol", "sulfide"]]
        .sum(axis=1)
        > 0
    ).astype(int)
    result["has_carbonyl_family"] = (
        result[["aldehyde", "ketone", "carboxylic_acid", "ester", "amide"]].sum(axis=1) > 0
    ).astype(int)
    return result


def stereochemistry_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize stereochemical scaffolds."""
    result = data.copy()
    result["stereochemical_complexity_score"] = (
        result["stereocenters"]
        + result["double_bond_stereo_centers"]
        + result["chiral"]
    )
    return result


def structure_property_scaffold(data: pd.DataFrame) -> pd.DataFrame:
    """Create simple structure-property descriptor scores."""
    result = data.copy()
    result["polarity_score"] = (
        result["heteroatom_count"]
        + result["hydrogen_bond_donors"]
        + result["hydrogen_bond_acceptors"]
    )
    result["hydrophobic_skeleton_score"] = result["carbon_count"] + result["ring_count"]
    result["complexity_score"] = (
        result["carbon_count"]
        + 2 * result["heteroatom_count"]
        + 2 * result["ring_count"]
        + 2 * result["aromatic_ring_count"]
        + 3 * result["stereocenter_count"]
    )
    result["druglike_descriptor_hint"] = (
        (result["carbon_count"] >= 5)
        & (result["heteroatom_count"] >= 1)
        & (result["hydrogen_bond_acceptors"] >= 1)
    ).astype(int)
    return result


def boltzmann_population(energies_kj_mol: list[float], temperature_k: float = 298.15) -> pd.DataFrame:
    """Calculate Boltzmann populations for conformer energies."""
    r_kj_mol_k = 0.008314462618
    weights = np.exp(-np.array(energies_kj_mol) / (r_kj_mol_k * temperature_k))
    populations = weights / weights.sum()
    return pd.DataFrame(
        {
            "conformer": [f"conf_{i+1}" for i in range(len(energies_kj_mol))],
            "energy_kj_mol": energies_kj_mol,
            "population": populations,
        }
    )


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
