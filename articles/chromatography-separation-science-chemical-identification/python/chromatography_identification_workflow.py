#!/usr/bin/env python3
"""
Synthetic chromatography workflow for separation metrics and candidate identification.

This script demonstrates:
1. Retention-factor calculation.
2. Adjacent-peak resolution.
3. Tentative retention-time candidate matching.
4. External calibration from peak areas.
5. Provenance-manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, stdev

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

def fit_linear_model(x: list[float], y: list[float]) -> dict[str, float]:
    x_bar = mean(x)
    y_bar = mean(y)
    numerator = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    denominator = sum((xi - x_bar) ** 2 for xi in x)
    slope = numerator / denominator
    intercept = y_bar - slope * x_bar
    predicted = [intercept + slope * xi for xi in x]
    residuals = [yi - yhat for yi, yhat in zip(y, predicted)]
    ss_residual = sum(r * r for r in residuals)
    ss_total = sum((yi - y_bar) ** 2 for yi in y)
    r_squared = 1.0 - ss_residual / ss_total
    return {
        "slope_area_per_mg_l": slope,
        "intercept_area": intercept,
        "r_squared": r_squared,
        "residual_standard_deviation": stdev(residuals),
    }

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    peaks = read_csv(DATA_DIR / "chromatographic_peaks.csv")
    library = read_csv(DATA_DIR / "reference_library.csv")
    calibration_rows = read_csv(DATA_DIR / "calibration_peak_areas.csv")
    metadata_rows = read_csv(DATA_DIR / "chromatography_metadata.csv")

    dead_time_min = 0.92
    tolerance_min = 0.08

    processed_peaks = []

    for row in peaks:
        retention_time = float(row["retention_time_min"])
        width = float(row["baseline_width_min"])
        processed_peaks.append({
            "peak_id": row["peak_id"],
            "sample_id": row["sample_id"],
            "retention_time_min": retention_time,
            "baseline_width_min": width,
            "peak_area": float(row["peak_area"]),
            "detector": row["detector"],
            "retention_factor_k": (retention_time - dead_time_min) / dead_time_min,
        })

    unknown_peaks = [row for row in processed_peaks if row["sample_id"] == "unknown_mix"]
    unknown_peaks = sorted(unknown_peaks, key=lambda r: r["retention_time_min"])

    resolution_rows = []
    for left, right in zip(unknown_peaks, unknown_peaks[1:]):
        resolution = (
            2.0
            * (right["retention_time_min"] - left["retention_time_min"])
            / (left["baseline_width_min"] + right["baseline_width_min"])
        )
        resolution_rows.append({
            "left_peak": left["peak_id"],
            "right_peak": right["peak_id"],
            "resolution_Rs": resolution,
        })

    candidate_rows = []
    for peak in unknown_peaks:
        for ref in library:
            delta = abs(
                peak["retention_time_min"]
                - float(ref["reference_retention_time_min"])
            )
            if delta <= tolerance_min:
                candidate_rows.append({
                    "peak_id": peak["peak_id"],
                    "candidate_compound": ref["compound"],
                    "retention_time_min": peak["retention_time_min"],
                    "reference_retention_time_min": float(ref["reference_retention_time_min"]),
                    "delta_min": delta,
                    "evidence_type": ref["evidence_type"],
                    "identification_status": "tentative retention-time match",
                })

    standards = [
        row for row in calibration_rows
        if row["standard_id"] == "blank" or row["standard_id"].startswith("std_")
    ]
    unknowns = [
        row for row in calibration_rows
        if row["standard_id"].startswith("unknown")
    ]

    x = [float(row["concentration_mg_l"]) for row in standards]
    y = [float(row["peak_area"]) for row in standards]
    calibration_model = fit_linear_model(x, y)

    unknown_estimates = []
    for row in unknowns:
        area = float(row["peak_area"])
        estimated_concentration = (
            area - calibration_model["intercept_area"]
        ) / calibration_model["slope_area_per_mg_l"]
        unknown_estimates.append({
            "standard_id": row["standard_id"],
            "compound": row["compound"],
            "peak_area": area,
            "estimated_concentration_mg_l": estimated_concentration,
        })

    write_csv(
        TABLE_DIR / "chromatographic_peak_metrics.csv",
        processed_peaks,
        [
            "peak_id",
            "sample_id",
            "retention_time_min",
            "baseline_width_min",
            "peak_area",
            "detector",
            "retention_factor_k",
        ],
    )

    write_csv(
        TABLE_DIR / "adjacent_peak_resolution.csv",
        resolution_rows,
        ["left_peak", "right_peak", "resolution_Rs"],
    )

    write_csv(
        TABLE_DIR / "tentative_candidate_matches.csv",
        candidate_rows,
        [
            "peak_id",
            "candidate_compound",
            "retention_time_min",
            "reference_retention_time_min",
            "delta_min",
            "evidence_type",
            "identification_status",
        ],
    )

    write_csv(
        TABLE_DIR / "calibration_unknown_estimates.csv",
        unknown_estimates,
        ["standard_id", "compound", "peak_area", "estimated_concentration_mg_l"],
    )

    manifest = {
        "article": "Chromatography, Separation Science, and Chemical Identification",
        "data_type": "synthetic educational chromatographic data",
        "dead_time_min": dead_time_min,
        "retention_time_tolerance_min": tolerance_min,
        "peak_count": len(processed_peaks),
        "candidate_match_count": len(candidate_rows),
        "metadata_record_count": len(metadata_rows),
        "calibration_model": calibration_model,
        "mean_unknown_concentration_mg_l": mean([
            row["estimated_concentration_mg_l"] for row in unknown_estimates
        ]),
        "responsible_use": "Synthetic educational data only; retention-time matching alone is not definitive chemical identification.",
    }

    with (MANIFEST_DIR / "chromatography_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "chromatography_audit_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Chromatography Audit Report\n\n")
        handle.write("Synthetic educational chromatography workflow.\n\n")
        handle.write("## Calibration Model\n\n")
        for key, value in calibration_model.items():
            handle.write(f"- **{key}:** {value:.8g}\n")
        handle.write("\n## Candidate Matches\n\n")
        for row in candidate_rows:
            handle.write(
                f"- {row['peak_id']}: {row['candidate_compound']} "
                f"(delta {row['delta_min']:.3f} min; {row['identification_status']})\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Retention-time matching alone is not definitive identification. Real workflows require reference standards, spectral evidence, method validation, uncertainty analysis, and expert review.\n")

    print("Chromatography workflow complete.")

if __name__ == "__main__":
    main()
