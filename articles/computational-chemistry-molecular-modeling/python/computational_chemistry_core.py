"""
Core utilities for computational chemistry and molecular modeling workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math
from itertools import combinations

import numpy as np
import pandas as pd


R_J_MOL_K = 8.314462618
KB_J_K = 1.380649e-23
H_J_S = 6.62607015e-34


def descriptor_table(descriptors: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple descriptor scaffolds."""
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


def conformer_boltzmann(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Boltzmann populations by molecule."""
    rows = []

    for molecule, group in data.groupby("molecule"):
        temperature = float(group["temperature_K"].iloc[0])
        weights = np.exp(
            -(group["relative_energy_kj_mol"].to_numpy(dtype=float) * 1000.0)
            / (R_J_MOL_K * temperature)
        )
        populations = weights / weights.sum()

        temp = group.copy()
        temp["boltzmann_weight"] = weights
        temp["population"] = populations
        rows.append(temp)

    return pd.concat(rows, ignore_index=True)


def lennard_jones(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Lennard-Jones potential energies."""
    result = data.copy()
    ratio = result["sigma"] / result["distance"]
    result["lj_energy"] = 4.0 * result["epsilon"] * (ratio ** 12 - ratio ** 6)
    return result


def tanimoto_similarity_from_fingerprints(fingerprints: pd.DataFrame) -> pd.DataFrame:
    """Calculate pairwise Tanimoto similarity for binary fingerprints."""
    bit_cols = [col for col in fingerprints.columns if col.startswith("bit_")]
    rows = []

    for _, row_a in fingerprints.iterrows():
        for _, row_b in fingerprints.iterrows():
            if row_a["molecule"] >= row_b["molecule"]:
                continue

            a_bits = row_a[bit_cols].to_numpy(dtype=int)
            b_bits = row_b[bit_cols].to_numpy(dtype=int)

            a = int(np.sum(a_bits == 1))
            b = int(np.sum(b_bits == 1))
            c = int(np.sum((a_bits == 1) & (b_bits == 1)))

            tanimoto = c / (a + b - c) if (a + b - c) else 0.0

            rows.append(
                {
                    "molecule_a": row_a["molecule"],
                    "molecule_b": row_b["molecule"],
                    "features_a": a,
                    "features_b": b,
                    "shared_features": c,
                    "tanimoto": tanimoto,
                }
            )

    return pd.DataFrame(rows)


def reaction_energy_table(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate reaction energies and activation barriers."""
    result = data.copy()
    result["reaction_energy_kj_mol"] = (
        result["product_energy_kj_mol"] - result["reactant_energy_kj_mol"]
    )
    result["activation_energy_kj_mol"] = (
        result["transition_state_energy_kj_mol"] - result["reactant_energy_kj_mol"]
    )
    result["exergonic_hint"] = (result["reaction_energy_kj_mol"] < 0).astype(int)
    return result


def toy_md_step(data: pd.DataFrame, dt: float = 0.5) -> pd.DataFrame:
    """Perform one simple velocity-Verlet-like educational update in one dimension."""
    result = data.copy()
    result["acceleration"] = result["force"] / result["mass"]
    result["new_velocity"] = result["velocity"] + result["acceleration"] * dt
    result["new_position"] = result["position"] + result["new_velocity"] * dt
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
