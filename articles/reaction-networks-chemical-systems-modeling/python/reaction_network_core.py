"""
Core utilities for reaction networks and chemical systems modeling.

All examples are simplified and educational.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math

import numpy as np
import pandas as pd


def load_stoichiometric_matrix(article_dir: Path) -> tuple[list[str], list[str], np.ndarray]:
    """Load the stoichiometric matrix from CSV."""
    stoich = pd.read_csv(article_dir / "data" / "stoichiometry.csv")
    species = stoich["species_id"].tolist()
    reaction_ids = [col for col in stoich.columns if col != "species_id"]
    matrix = stoich[reaction_ids].to_numpy(dtype=float)
    return species, reaction_ids, matrix


def build_stoichiometric_table(article_dir: Path) -> pd.DataFrame:
    """Build a long-form stoichiometric table."""
    stoich = pd.read_csv(article_dir / "data" / "stoichiometry.csv")
    return stoich


def network_rates(concentration: np.ndarray, parameters: dict[str, float]) -> np.ndarray:
    """
    Calculate rates for a small example network:

    r1: A -> B
    r2: B -> C
    r3: A -> D
    r4: B -> E
    """
    A, B, C, D, E = concentration

    return np.array(
        [
            parameters["k1_A_to_B"] * A,
            parameters["k2_B_to_C"] * B,
            parameters["k3_A_to_D"] * A,
            parameters["k4_B_to_E"] * B,
        ],
        dtype=float,
    )


def simulate_network_case(row: pd.Series, stoich: np.ndarray) -> pd.DataFrame:
    """Simulate a five-species, four-reaction network using Euler integration."""
    concentration = np.array(
        [row["A0"], row["B0"], row["C0"], row["D0"], row["E0"]],
        dtype=float,
    )

    parameters = {
        "k1_A_to_B": row["k1_A_to_B"],
        "k2_B_to_C": row["k2_B_to_C"],
        "k3_A_to_D": row["k3_A_to_D"],
        "k4_B_to_E": row["k4_B_to_E"],
    }

    times = np.arange(0.0, row["total_time"] + row["time_step"], row["time_step"])
    dt = float(row["time_step"])

    rows = []

    for time_value in times:
        rates = network_rates(concentration, parameters)
        rows.append(
            {
                "case_id": row["case_id"],
                "time": float(time_value),
                "A": concentration[0],
                "B": concentration[1],
                "C": concentration[2],
                "D": concentration[3],
                "E": concentration[4],
                "r1_A_to_B": rates[0],
                "r2_B_to_C": rates[1],
                "r3_A_to_D": rates[2],
                "r4_B_to_E": rates[3],
            }
        )

        dc_dt = stoich @ rates
        concentration = np.maximum(concentration + dc_dt * dt, 0.0)

    return pd.DataFrame(rows)


def simulate_network_cases(data: pd.DataFrame, stoich: np.ndarray) -> pd.DataFrame:
    """Simulate all network cases."""
    frames = [simulate_network_case(row, stoich) for _, row in data.iterrows()]
    return pd.concat(frames, ignore_index=True)


def parallel_selectivity(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate selectivity for A -> B and A -> C parallel pathways."""
    result = data.copy()
    result["fraction_to_B"] = result["k_to_B"] / (result["k_to_B"] + result["k_to_C"])
    result["fraction_to_C"] = result["k_to_C"] / (result["k_to_B"] + result["k_to_C"])
    result["B_to_C_selectivity"] = result["fraction_to_B"] / result["fraction_to_C"]
    return result


def final_branching_outcomes(trajectory: pd.DataFrame) -> pd.DataFrame:
    """Summarize final product distribution for simulated network cases."""
    rows = []

    for case_id, group in trajectory.groupby("case_id"):
        final = group.sort_values("time").tail(1).iloc[0]
        total_products = final["C"] + final["D"] + final["E"]

        rows.append(
            {
                "case_id": case_id,
                "final_A": final["A"],
                "final_B": final["B"],
                "final_C": final["C"],
                "final_D": final["D"],
                "final_E": final["E"],
                "fraction_product_C": final["C"] / total_products if total_products > 0 else 0.0,
                "fraction_product_D": final["D"] / total_products if total_products > 0 else 0.0,
                "fraction_product_E": final["E"] / total_products if total_products > 0 else 0.0,
            }
        )

    return pd.DataFrame(rows)


def flux_table_from_state(concentration: dict[str, float], parameters: dict[str, float], stoich: np.ndarray) -> pd.DataFrame:
    """Calculate species flux contributions at a single state."""
    c = np.array(
        [
            concentration["A"],
            concentration["B"],
            concentration["C"],
            concentration["D"],
            concentration["E"],
        ],
        dtype=float,
    )

    rates = network_rates(c, parameters)
    flux_matrix = stoich * rates

    species = ["A", "B", "C", "D", "E"]
    reactions = ["r1_A_to_B", "r2_B_to_C", "r3_A_to_D", "r4_B_to_E"]

    rows = []
    for i, species_id in enumerate(species):
        for j, reaction_id in enumerate(reactions):
            rows.append(
                {
                    "species_id": species_id,
                    "reaction_id": reaction_id,
                    "flux_contribution": flux_matrix[i, j],
                }
            )

    return pd.DataFrame(rows)


def sensitivity_analysis(data: pd.DataFrame, stoich: np.ndarray) -> pd.DataFrame:
    """Estimate finite-difference sensitivity of final C concentration to k1."""
    rows = []

    for _, row in data.iterrows():
        def run_case(k1_value: float) -> float:
            simulation_row = pd.Series(
                {
                    "case_id": row["case_id"],
                    "k1_A_to_B": k1_value,
                    "k2_B_to_C": row["k2"],
                    "k3_A_to_D": row["k3"],
                    "k4_B_to_E": row["k4"],
                    "A0": 1.0,
                    "B0": 0.0,
                    "C0": 0.0,
                    "D0": 0.0,
                    "E0": 0.0,
                    "total_time": row["total_time"],
                    "time_step": row["time_step"],
                }
            )
            trajectory = simulate_network_case(simulation_row, stoich)
            return float(trajectory.sort_values("time").tail(1)["C"].iloc[0])

        c_low = run_case(row["base_k1"] - row["delta"])
        c_high = run_case(row["base_k1"] + row["delta"])
        sensitivity = (c_high - c_low) / (2.0 * row["delta"])

        rows.append(
            {
                "case_id": row["case_id"],
                "base_k1": row["base_k1"],
                "delta": row["delta"],
                "final_C_low": c_low,
                "final_C_high": c_high,
                "sensitivity_dCfinal_dk1": sensitivity,
            }
        )

    return pd.DataFrame(rows)


def simple_fit_first_order_decay(data: pd.DataFrame) -> pd.DataFrame:
    """Fit A(t) = A0 exp(-k t) from observed decay data."""
    clean = data.copy()
    clean["ln_A"] = np.log(clean["A_observed"])
    slope, intercept = np.polyfit(clean["time"], clean["ln_A"], deg=1)

    return pd.DataFrame(
        [
            {
                "estimated_k_total": -slope,
                "estimated_A0": math.exp(intercept),
                "interpretation": "This fits total first-order disappearance of A, not unique pathway rates.",
            }
        ]
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
