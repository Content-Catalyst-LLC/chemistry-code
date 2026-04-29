#!/usr/bin/env python3
"""
Synthetic semiconductor, electronic, and photochemical materials workflow.

This script demonstrates:
1. Band-gap and absorption-edge checks.
2. Charge-transport proxy calculations.
3. Photostability and critical-material review flags.
4. Device-like replicate summaries.
5. Photostability time-series degradation summaries.
6. Electronic and photochemical materials manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
REPORT_DIR = BASE_DIR / "outputs" / "reports"
MANIFEST_DIR = BASE_DIR / "outputs" / "manifests"

TARGETS = {
    "band_gap_eV": 1.6,
    "photostability_score": 0.90,
    "mobility_balance_ratio": 0.50,
    "processing_temperature_C": 150.0,
}

WEIGHTS = {
    "band_gap_eV": 1.4,
    "photostability_score": 1.5,
    "mobility_balance_ratio": 0.9,
    "processing_temperature_C": 0.7,
}

SCALES = {
    "band_gap_eV": 0.50,
    "photostability_score": 0.25,
    "mobility_balance_ratio": 0.50,
    "processing_temperature_C": 350.0,
}

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
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

    materials = read_csv(DATA_DIR / "material_candidates.csv")
    device_runs = read_csv(DATA_DIR / "device_runs.csv")
    photostability = read_csv(DATA_DIR / "photostability_time_series.csv")
    spectroscopy = read_csv(DATA_DIR / "spectroscopy_measurements.csv")
    interfaces = read_csv(DATA_DIR / "interface_records.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")

    lifecycle_lookup = {row["material_id"]: row for row in lifecycle}

    screening_rows = []

    for row in materials:
        band_gap = float(row["band_gap_eV"])
        electron_mobility = float(row["electron_mobility_cm2_V_s"])
        hole_mobility = float(row["hole_mobility_cm2_V_s"])
        lifetime = float(row["carrier_lifetime_ns"])
        edge_nm = float(row["absorption_edge_nm"])
        photostability_score = float(row["photostability_score"])
        processing_temperature = float(row["processing_temperature_C"])
        critical_material = as_bool(row["critical_material_flag"])

        edge_band_gap_estimate = 1240.0 / edge_nm
        mobility_balance_ratio = min(electron_mobility, hole_mobility) / max(electron_mobility, hole_mobility)
        transport_proxy = (electron_mobility + hole_mobility) * lifetime

        values = {
            "band_gap_eV": band_gap,
            "photostability_score": photostability_score,
            "mobility_balance_ratio": mobility_balance_ratio,
            "processing_temperature_C": processing_temperature,
        }

        score = 0.0
        score_terms = {}

        for property_name, target_value in TARGETS.items():
            term = WEIGHTS[property_name] * ((values[property_name] - target_value) / SCALES[property_name]) ** 2
            score_terms[property_name] = term
            score += term

        lifecycle_row = lifecycle_lookup.get(row["material_id"], {})
        lifecycle_review = as_bool(lifecycle_row.get("responsible_design_review", "false"))

        stability_review = photostability_score < 0.60
        processing_review = processing_temperature > 500
        responsible_review = critical_material or stability_review or processing_review or lifecycle_review

        critical_material_penalty = 0.6 if critical_material else 0.0
        screening_score = score + critical_material_penalty

        screening_rows.append({
            "material_id": row["material_id"],
            "material_class": row["material_class"],
            "band_gap_eV": band_gap,
            "edge_band_gap_estimate_eV": edge_band_gap_estimate,
            "electron_mobility_cm2_V_s": electron_mobility,
            "hole_mobility_cm2_V_s": hole_mobility,
            "carrier_lifetime_ns": lifetime,
            "transport_proxy": transport_proxy,
            "mobility_balance_ratio": mobility_balance_ratio,
            "photostability_score": photostability_score,
            "processing_temperature_C": processing_temperature,
            "critical_material_flag": critical_material,
            "stability_review_required": stability_review,
            "processing_review_required": processing_review,
            "lifecycle_review_required": lifecycle_review,
            "responsible_design_review_required": responsible_review,
            "screening_score": screening_score,
        })

    screening_rows.sort(key=lambda row: row["screening_score"])
    for index, row in enumerate(screening_rows, start=1):
        row["rank"] = index

    device_groups: dict[str, list[dict[str, str]]] = {}
    for row in device_runs:
        device_groups.setdefault(row["material_id"], []).append(row)

    device_summary = []
    for material_id, rows in sorted(device_groups.items()):
        currents = [float(row["photocurrent_mA_cm2"]) for row in rows]
        voltages = [float(row["open_circuit_voltage_V"]) for row in rows]
        fill_factors = [float(row["fill_factor"]) for row in rows]
        stability_scores = [float(row["photostability_score"]) for row in rows]

        mean_current = mean(currents)
        mean_voltage = mean(voltages)
        mean_fill_factor = mean(fill_factors)

        device_summary.append({
            "material_id": material_id,
            "mean_photocurrent_mA_cm2": mean_current,
            "mean_open_circuit_voltage_V": mean_voltage,
            "mean_fill_factor": mean_fill_factor,
            "performance_proxy": mean_current * mean_voltage * mean_fill_factor,
            "mean_photostability_score": mean(stability_scores),
            "replicate_count": len(rows),
        })

    stability_groups: dict[str, list[dict[str, str]]] = {}
    for row in photostability:
        stability_groups.setdefault(row["material_id"], []).append(row)

    stability_summary = []
    for material_id, rows in sorted(stability_groups.items()):
        sorted_rows = sorted(rows, key=lambda r: float(r["illumination_hours"]))
        hours = [float(row["illumination_hours"]) for row in sorted_rows]
        performance = [float(row["normalized_performance"]) for row in sorted_rows]
        slope = fit_linear_slope(hours, performance)
        loss = 100.0 * (performance[0] - performance[-1]) / performance[0]

        stability_summary.append({
            "material_id": material_id,
            "degradation_slope_per_hour": slope,
            "initial_performance": performance[0],
            "final_performance": performance[-1],
            "percent_performance_loss": loss,
            "measurement_count": len(rows),
        })

    review_rows = [
        row for row in screening_rows
        if row["responsible_design_review_required"]
    ]

    write_csv(
        TABLE_DIR / "electronic_photochemical_materials_screening_ranked.csv",
        screening_rows,
        [
            "material_id",
            "material_class",
            "band_gap_eV",
            "edge_band_gap_estimate_eV",
            "electron_mobility_cm2_V_s",
            "hole_mobility_cm2_V_s",
            "carrier_lifetime_ns",
            "transport_proxy",
            "mobility_balance_ratio",
            "photostability_score",
            "processing_temperature_C",
            "critical_material_flag",
            "stability_review_required",
            "processing_review_required",
            "lifecycle_review_required",
            "responsible_design_review_required",
            "screening_score",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "device_replicate_summary.csv",
        device_summary,
        [
            "material_id",
            "mean_photocurrent_mA_cm2",
            "mean_open_circuit_voltage_V",
            "mean_fill_factor",
            "performance_proxy",
            "mean_photostability_score",
            "replicate_count",
        ],
    )

    write_csv(
        TABLE_DIR / "photostability_degradation_summary.csv",
        stability_summary,
        [
            "material_id",
            "degradation_slope_per_hour",
            "initial_performance",
            "final_performance",
            "percent_performance_loss",
            "measurement_count",
        ],
    )

    write_csv(
        TABLE_DIR / "responsible_design_review.csv",
        review_rows,
        [
            "material_id",
            "material_class",
            "critical_material_flag",
            "stability_review_required",
            "processing_review_required",
            "lifecycle_review_required",
            "responsible_design_review_required",
            "rank",
        ],
    )

    manifest = {
        "article": "Semiconductor, Electronic, and Photochemical Materials",
        "data_type": "synthetic educational electronic and photochemical materials data",
        "target_profile": TARGETS,
        "weights": WEIGHTS,
        "scales": SCALES,
        "candidate_count": len(materials),
        "device_run_count": len(device_runs),
        "photostability_record_count": len(photostability),
        "spectroscopy_record_count": len(spectroscopy),
        "interface_record_count": len(interfaces),
        "lifecycle_note_count": len(lifecycle),
        "best_candidate": screening_rows[0]["material_id"],
        "responsible_design_review_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for device certification, photovoltaic claims, photochemical safety, procurement, environmental claims, industrial process design, or regulatory use.",
    }

    with (MANIFEST_DIR / "electronic_photochemical_materials_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "electronic_photochemical_materials_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Electronic and Photochemical Materials Report\n\n")
        handle.write("Synthetic educational semiconductor, electronic, and photochemical materials workflow.\n\n")
        handle.write("## Candidate Ranking\n\n")
        for row in screening_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['material_id']} "
                f"({row['material_class']}), score={row['screening_score']:.4g}, "
                f"review={row['responsible_design_review_required']}\n"
            )
        handle.write("\n## Photostability Summary\n\n")
        for row in stability_summary:
            handle.write(
                f"- {row['material_id']}: final performance={row['final_performance']:.3f}, "
                f"loss={row['percent_performance_loss']:.2f}%\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real materials decisions require validated measurements, device testing, uncertainty, stability analysis, and lifecycle review.\n")

    print("Electronic and photochemical materials workflow complete.")

if __name__ == "__main__":
    main()
