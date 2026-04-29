"""
Core utilities for molecular dynamics and chemical simulation workflows.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import numpy as np
import pandas as pd


COULOMB_CONSTANT_SIMPLIFIED = 138.935456


def velocity_verlet_step(data: pd.DataFrame, dt: float = 0.5) -> pd.DataFrame:
    """Perform one simple one-dimensional velocity-Verlet-style update."""
    result = data.copy()
    result["acceleration"] = result["force"] / result["mass"]
    result["new_position"] = (
        result["position"]
        + result["velocity"] * dt
        + 0.5 * result["acceleration"] * dt**2
    )
    result["new_velocity"] = result["velocity"] + result["acceleration"] * dt
    result["kinetic_energy_initial"] = 0.5 * result["mass"] * result["velocity"] ** 2
    result["kinetic_energy_updated"] = 0.5 * result["mass"] * result["new_velocity"] ** 2
    return result


def lennard_jones(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate Lennard-Jones potential energies."""
    result = data.copy()
    ratio = result["sigma"] / result["distance"]
    result["lj_energy"] = 4.0 * result["epsilon"] * (ratio ** 12 - ratio ** 6)
    return result


def coulomb_energy(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate simplified Coulomb interaction energies in MD-style units."""
    result = data.copy()
    result["coulomb_energy"] = (
        COULOMB_CONSTANT_SIMPLIFIED
        * result["charge_i"]
        * result["charge_j"]
        / (result["dielectric"] * result["distance"])
    )
    return result


def trajectory_msd(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate mean-squared displacement relative to first frame."""
    result = data.copy()
    x0, y0, z0 = result.loc[0, ["x", "y", "z"]]
    result["msd"] = (
        (result["x"] - x0) ** 2
        + (result["y"] - y0) ** 2
        + (result["z"] - z0) ** 2
    )
    result["diffusion_estimate"] = np.where(
        result["time_ps"] > 0,
        result["msd"] / (6.0 * result["time_ps"]),
        np.nan,
    )
    return result


def rdf_histogram(data: pd.DataFrame, bin_width: float = 0.5, r_max: float = 3.5) -> pd.DataFrame:
    """Create a simple RDF-like distance histogram scaffold."""
    bins = np.arange(0.5, r_max + bin_width, bin_width)
    counts, edges = np.histogram(data["distance"], bins=bins)
    midpoints = 0.5 * (edges[:-1] + edges[1:])
    shell_volume_proxy = 4.0 * np.pi * midpoints**2 * bin_width
    normalized_count_proxy = counts / np.where(shell_volume_proxy > 0, shell_volume_proxy, np.nan)

    return pd.DataFrame(
        {
            "r_midpoint": midpoints,
            "count": counts,
            "shell_volume_proxy": shell_volume_proxy,
            "normalized_count_proxy": normalized_count_proxy,
        }
    )


def ensemble_metadata(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize ensemble protocol metadata."""
    result = data.copy()
    result["total_steps_estimate"] = (
        result["production_ns"] * 1_000_000.0 / result["timestep_fs"]
    )
    return result


def trajectory_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize trajectory metadata."""
    result = data.copy()
    result["atom_ns_product"] = result["atoms"] * result["production_ns"]
    result["large_system_hint"] = (result["atoms"] >= 50000).astype(int)
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
