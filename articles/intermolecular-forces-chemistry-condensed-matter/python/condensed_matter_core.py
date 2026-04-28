"""
Core utilities for intermolecular forces and condensed-matter chemistry.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


R_GAS_CONSTANT_J_MOL_K = 8.314462618


def lennard_jones_potential(r_angstrom: np.ndarray, epsilon_kj_mol: float, sigma_angstrom: float) -> np.ndarray:
    """Calculate Lennard-Jones potential energy in kJ/mol."""
    ratio = sigma_angstrom / r_angstrom
    return 4.0 * epsilon_kj_mol * (ratio ** 12 - ratio ** 6)


def lennard_jones_table(parameters: pd.DataFrame) -> pd.DataFrame:
    """Generate Lennard-Jones potential tables for multiple simplified pairs."""
    rows = []

    for _, row in parameters.iterrows():
        r_values = np.linspace(row["sigma_angstrom"] * 0.85, row["sigma_angstrom"] * 3.0, 160)
        u_values = lennard_jones_potential(
            r_values,
            float(row["epsilon_kj_mol"]),
            float(row["sigma_angstrom"]),
        )

        for r_value, u_value in zip(r_values, u_values):
            rows.append(
                {
                    "pair": row["pair"],
                    "r_angstrom": float(r_value),
                    "u_kj_mol": float(u_value),
                }
            )

    return pd.DataFrame(rows)


def lennard_jones_minima(potential_table: pd.DataFrame) -> pd.DataFrame:
    """Find approximate potential minima for each pair."""
    rows = []

    for pair, group in potential_table.groupby("pair"):
        idx = group["u_kj_mol"].idxmin()
        minimum = group.loc[idx]
        rows.append(
            {
                "pair": pair,
                "r_min_angstrom": float(minimum["r_angstrom"]),
                "u_min_kj_mol": float(minimum["u_kj_mol"]),
            }
        )

    return pd.DataFrame(rows)


def fit_vapor_pressure(vapor: pd.DataFrame) -> pd.DataFrame:
    """Fit ln(P) versus 1/T and estimate an apparent enthalpy of vaporization."""
    result = vapor.copy()
    result["inverse_temperature_K_inv"] = 1.0 / result["temperature_K"]
    result["ln_pressure_kPa"] = np.log(result["pressure_kPa"])

    x = result["inverse_temperature_K_inv"].to_numpy()
    y = result["ln_pressure_kPa"].to_numpy()
    slope, intercept = np.polyfit(x, y, deg=1)

    estimated_delta_h_j_mol = -slope * R_GAS_CONSTANT_J_MOL_K

    fit = pd.DataFrame(
        [
            {
                "substance": result["substance"].iloc[0],
                "slope": float(slope),
                "intercept": float(intercept),
                "estimated_delta_h_vap_kj_mol": float(estimated_delta_h_j_mol / 1000.0),
            }
        ]
    )

    return result, fit


def radial_distribution_scaffold(coordinates: pd.DataFrame) -> pd.DataFrame:
    """Create a pair-distance histogram scaffold from particle coordinates."""
    coords = coordinates[["x_nm", "y_nm", "z_nm"]].to_numpy(dtype=float)
    distances = []

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            distances.append(float(np.linalg.norm(coords[i] - coords[j])))

    hist, edges = np.histogram(distances, bins=np.linspace(0.0, 5.0, 11))

    return pd.DataFrame(
        {
            "r_lower_nm": edges[:-1],
            "r_upper_nm": edges[1:],
            "pair_count": hist,
        }
    )


def summarize_phase_properties(phase: pd.DataFrame, surface: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Summarize simplified phase and surface-tension properties."""
    by_phase = (
        phase.groupby("phase_at_room_conditions")
        .size()
        .reset_index(name="count")
        .sort_values("phase_at_room_conditions")
    )

    by_interaction = (
        phase.groupby("dominant_interaction")
        .size()
        .reset_index(name="count")
        .sort_values(["count", "dominant_interaction"], ascending=[False, True])
    )

    surface_summary = (
        surface.groupby("dominant_interaction", as_index=False)
        .agg(
            mean_surface_tension_mN_m=("surface_tension_mN_m", "mean"),
            liquid_count=("liquid", "count"),
        )
        .sort_values("mean_surface_tension_mN_m", ascending=False)
    )

    return {
        "by_phase": by_phase,
        "by_interaction": by_interaction,
        "surface_summary": surface_summary,
    }


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
