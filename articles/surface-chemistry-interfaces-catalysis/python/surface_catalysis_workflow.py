#!/usr/bin/env python3
"""
Synthetic surface chemistry and catalysis workflow.

This script demonstrates:
1. Competitive Langmuir coverage calculations.
2. Simplified catalytic rate proxies.
3. Catalyst ranking with selectivity and critical-material flags.
4. Deactivation summaries.
5. Surface-characterization and lifecycle provenance.
6. Surface-catalysis manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
REPORT_DIR = BASE_DIR / "outputs" / "reports"
MANIFEST_DIR = BASE_DIR / "outputs" / "manifests"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}

def fit_linear_slope(x_values: list[float], y_values: list[float]) -> float:
    x_bar = mean(x_values)
    y_bar = mean(y_values)
    numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(x_values, y_values))
    denominator = sum((x - x_bar) ** 2 for x in x_values)
    return numerator / denominator

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    catalysts = read_csv(DATA_DIR / "catalyst_candidates.csv")
    adsorption = read_csv(DATA_DIR / "adsorption_isotherm.csv")
    performance = read_csv(DATA_DIR / "catalyst_performance.csv")
    deactivation = read_csv(DATA_DIR / "deactivation_time_series.csv")
    characterization = read_csv(DATA_DIR / "surface_characterization.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")
    interfaces = read_csv(DATA_DIR / "interface_records.csv")

    lifecycle_lookup = {row["catalyst_id"]: row for row in lifecycle}

    P_A = 1.0
    P_B = 0.5
    temperature_K = 550.0
    R_kJ_mol_K = 0.008314
    pre_exponential = 1.0e5

    screening_rows = []

    for row in catalysts:
        denominator = (
            1.0
            + float(row["K_A_bar_inv"]) * P_A
            + float(row["K_B_bar_inv"]) * P_B
        )

        theta_A = float(row["K_A_bar_inv"]) * P_A / denominator
        theta_B = float(row["K_B_bar_inv"]) * P_B / denominator

        k = pre_exponential * math.exp(
            -float(row["activation_energy_kJ_mol"]) / (R_kJ_mol_K * temperature_K)
        )

        rate_proxy = k * theta_A * theta_B * float(row["site_density_umol_g"])
        critical_flag = as_bool(row["critical_metal_flag"])
        lifecycle_row = lifecycle_lookup.get(row["catalyst_id"], {})
        sustainability_review = as_bool(lifecycle_row.get("sustainability_review_required", "false"))

        screening_score = (
            0.45 * rate_proxy
            + 20.0 * float(row["selectivity_target"])
            + 0.02 * float(row["surface_area_m2_g"])
            - (15.0 if critical_flag else 0.0)
            - (5.0 if sustainability_review else 0.0)
        )

        screening_rows.append({
            "catalyst_id": row["catalyst_id"],
            "catalyst_class": row["catalyst_class"],
            "theta_A": theta_A,
            "theta_B": theta_B,
            "surface_rate_proxy": rate_proxy,
            "selectivity_target": float(row["selectivity_target"]),
            "surface_area_m2_g": float(row["surface_area_m2_g"]),
            "critical_metal_flag": critical_flag,
            "sustainability_review_required": sustainability_review,
            "screening_score": screening_score,
        })

    screening_rows.sort(key=lambda row: row["screening_score"], reverse=True)
    for rank, row in enumerate(screening_rows, start=1):
        row["rank"] = rank

    deactivation_groups: dict[str, list[dict[str, str]]] = {}
    for row in deactivation:
        deactivation_groups.setdefault(row["catalyst_id"], []).append(row)

    deactivation_rows = []
    for catalyst_id, rows in sorted(deactivation_groups.items()):
        rows_sorted = sorted(rows, key=lambda r: float(r["time_h"]))
        times = [float(r["time_h"]) for r in rows_sorted]
        rates = [float(r["normalized_rate"]) for r in rows_sorted]
        slope = fit_linear_slope(times, rates)
        percent_loss = 100.0 * (rates[0] - rates[-1]) / rates[0]

        deactivation_rows.append({
            "catalyst_id": catalyst_id,
            "deactivation_slope_per_h": slope,
            "initial_rate": rates[0],
            "final_rate": rates[-1],
            "percent_rate_loss": percent_loss,
        })

    performance_groups: dict[str, list[dict[str, str]]] = {}
    for row in performance:
        performance_groups.setdefault(row["catalyst_id"], []).append(row)

    performance_rows = []
    for catalyst_id, rows in sorted(performance_groups.items()):
        conversions = [float(r["conversion_percent"]) for r in rows]
        selectivities = [float(r["selectivity_percent"]) for r in rows]
        performance_rows.append({
            "catalyst_id": catalyst_id,
            "mean_conversion_percent": mean(conversions),
            "mean_selectivity_percent": mean(selectivities),
            "replicate_count": len(rows),
        })

    write_csv(
        TABLE_DIR / "surface_catalyst_screening_ranked.csv",
        screening_rows,
        [
            "catalyst_id",
            "catalyst_class",
            "theta_A",
            "theta_B",
            "surface_rate_proxy",
            "selectivity_target",
            "surface_area_m2_g",
            "critical_metal_flag",
            "sustainability_review_required",
            "screening_score",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "catalyst_deactivation_summary.csv",
        deactivation_rows,
        ["catalyst_id", "deactivation_slope_per_h", "initial_rate", "final_rate", "percent_rate_loss"],
    )

    write_csv(
        TABLE_DIR / "catalyst_performance_summary.csv",
        performance_rows,
        ["catalyst_id", "mean_conversion_percent", "mean_selectivity_percent", "replicate_count"],
    )

    manifest = {
        "article": "Surface Chemistry, Interfaces, and Catalysis",
        "data_type": "synthetic educational surface chemistry and catalysis data",
        "model": "competitive Langmuir coverage with simplified rate proxy",
        "pressure_A_bar": P_A,
        "pressure_B_bar": P_B,
        "temperature_K": temperature_K,
        "catalyst_count": len(catalysts),
        "adsorption_record_count": len(adsorption),
        "performance_record_count": len(performance),
        "deactivation_record_count": len(deactivation),
        "characterization_record_count": len(characterization),
        "lifecycle_note_count": len(lifecycle),
        "interface_record_count": len(interfaces),
        "best_candidate": screening_rows[0]["catalyst_id"],
        "responsible_use": "Synthetic educational data only; not validated for catalyst design, process engineering, environmental claims, or regulatory use.",
    }

    with (MANIFEST_DIR / "surface_catalysis_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "surface_catalysis_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Surface Catalysis Report\n\n")
        handle.write("Synthetic educational surface chemistry and catalysis workflow.\n\n")
        handle.write("## Catalyst Ranking\n\n")
        for row in screening_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['catalyst_id']} "
                f"({row['catalyst_class']}), score={row['screening_score']:.4g}, "
                f"critical metal={row['critical_metal_flag']}\n"
            )
        handle.write("\n## Deactivation Summary\n\n")
        for row in deactivation_rows:
            handle.write(
                f"- {row['catalyst_id']}: final rate={row['final_rate']:.3f}, "
                f"loss={row['percent_rate_loss']:.2f}%\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real catalyst evaluation requires validated mechanisms, transport checks, product analysis, stability testing, and safety review.\n")

    print("Surface catalysis workflow complete.")

if __name__ == "__main__":
    main()
