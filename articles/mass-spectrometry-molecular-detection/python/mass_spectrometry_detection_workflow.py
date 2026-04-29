#!/usr/bin/env python3
"""
Synthetic mass spectrometry workflow for molecular detection.

This script demonstrates:
1. Exact-mass candidate matching.
2. Mass-error calculations in ppm.
3. Isotope-spacing charge estimation.
4. MS/MS fragment summary.
5. Calibration from synthetic peak areas.
6. Provenance-manifest creation.

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
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
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
        "slope_area_per_ng_ml": slope,
        "intercept_area": intercept,
        "r_squared": r_squared,
        "residual_standard_deviation": stdev(residuals),
    }

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    features = read_csv(DATA_DIR / "ms_features.csv")
    candidates = read_csv(DATA_DIR / "candidate_library.csv")
    isotopes = read_csv(DATA_DIR / "isotope_clusters.csv")
    fragments = read_csv(DATA_DIR / "msms_fragments.csv")
    calibration_rows = read_csv(DATA_DIR / "ms_calibration.csv")
    metadata_rows = read_csv(DATA_DIR / "ms_metadata.csv")

    ppm_tolerance = 5.0
    match_rows = []

    for feature in features:
        for candidate in candidates:
            if int(feature["charge"]) != int(candidate["expected_charge"]):
                continue
            if feature["ion_mode"] != candidate["ion_mode"]:
                continue

            observed = float(feature["observed_mz"])
            theoretical = float(candidate["theoretical_mz"])
            ppm_error = (observed - theoretical) / theoretical * 1_000_000.0

            if abs(ppm_error) <= ppm_tolerance:
                match_rows.append({
                    "feature_id": feature["feature_id"],
                    "sample_id": feature["sample_id"],
                    "candidate_id": candidate["candidate_id"],
                    "candidate_name": candidate["candidate_name"],
                    "observed_mz": observed,
                    "theoretical_mz": theoretical,
                    "ppm_error": ppm_error,
                    "charge": int(feature["charge"]),
                    "retention_time_min": float(feature["retention_time_min"]),
                    "peak_area": float(feature["peak_area"]),
                    "identification_status": "tentative exact-mass match",
                })

    isotope_groups: dict[str, list[dict[str, str]]] = {}
    for row in isotopes:
        isotope_groups.setdefault(row["cluster_id"], []).append(row)

    charge_rows = []
    for cluster_id, rows in sorted(isotope_groups.items()):
        rows_sorted = sorted(rows, key=lambda r: float(r["mz"]))
        if len(rows_sorted) < 2:
            continue
        first_spacing = float(rows_sorted[1]["mz"]) - float(rows_sorted[0]["mz"])
        estimated_charge = round(1.0 / first_spacing)
        charge_rows.append({
            "cluster_id": cluster_id,
            "first_isotope_spacing_mz": first_spacing,
            "estimated_charge": estimated_charge,
        })

    fragment_summary: dict[str, dict[str, object]] = {}
    for row in fragments:
        feature_id = row["feature_id"]
        fragment_summary.setdefault(
            feature_id,
            {
                "feature_id": feature_id,
                "fragment_count": 0,
                "base_product_mz": None,
                "base_product_intensity": -1.0,
            },
        )
        fragment_summary[feature_id]["fragment_count"] += 1
        intensity = float(row["relative_intensity"])
        if intensity > fragment_summary[feature_id]["base_product_intensity"]:
            fragment_summary[feature_id]["base_product_intensity"] = intensity
            fragment_summary[feature_id]["base_product_mz"] = float(row["product_mz"])

    fragment_rows = list(fragment_summary.values())

    standards = [
        row for row in calibration_rows
        if row["standard_id"] == "blank" or row["standard_id"].startswith("std_")
    ]
    unknowns = [
        row for row in calibration_rows
        if row["standard_id"].startswith("unknown")
    ]

    x = [float(row["concentration_ng_ml"]) for row in standards]
    y = [float(row["peak_area"]) for row in standards]
    calibration_model = fit_linear_model(x, y)

    unknown_estimates = []
    for row in unknowns:
        area = float(row["peak_area"])
        estimated_concentration = (
            area - calibration_model["intercept_area"]
        ) / calibration_model["slope_area_per_ng_ml"]
        unknown_estimates.append({
            "standard_id": row["standard_id"],
            "compound": row["compound"],
            "peak_area": area,
            "estimated_concentration_ng_ml": estimated_concentration,
        })

    write_csv(
        TABLE_DIR / "tentative_exact_mass_matches.csv",
        match_rows,
        [
            "feature_id",
            "sample_id",
            "candidate_id",
            "candidate_name",
            "observed_mz",
            "theoretical_mz",
            "ppm_error",
            "charge",
            "retention_time_min",
            "peak_area",
            "identification_status",
        ],
    )

    write_csv(
        TABLE_DIR / "isotope_charge_estimates.csv",
        charge_rows,
        ["cluster_id", "first_isotope_spacing_mz", "estimated_charge"],
    )

    write_csv(
        TABLE_DIR / "msms_fragment_summary.csv",
        fragment_rows,
        ["feature_id", "fragment_count", "base_product_mz", "base_product_intensity"],
    )

    write_csv(
        TABLE_DIR / "ms_quant_unknown_estimates.csv",
        unknown_estimates,
        ["standard_id", "compound", "peak_area", "estimated_concentration_ng_ml"],
    )

    manifest = {
        "article": "Mass Spectrometry and Molecular Detection",
        "data_type": "synthetic educational mass spectrometry data",
        "ppm_tolerance": ppm_tolerance,
        "feature_count": len(features),
        "candidate_count": len(candidates),
        "tentative_match_count": len(match_rows),
        "isotope_cluster_count": len(charge_rows),
        "fragment_feature_count": len(fragment_rows),
        "metadata_record_count": len(metadata_rows),
        "calibration_model": calibration_model,
        "mean_unknown_concentration_ng_ml": mean([
            row["estimated_concentration_ng_ml"] for row in unknown_estimates
        ]),
        "responsible_use": "Synthetic educational data only; exact mass alone is not definitive molecular identification.",
    }

    with (MANIFEST_DIR / "mass_spectrometry_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "mass_spectrometry_audit_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Mass Spectrometry Audit Report\n\n")
        handle.write("Synthetic educational mass spectrometry workflow.\n\n")
        handle.write("## Calibration Model\n\n")
        for key, value in calibration_model.items():
            handle.write(f"- **{key}:** {value:.8g}\n")
        handle.write("\n## Tentative Exact-Mass Matches\n\n")
        for row in match_rows:
            handle.write(
                f"- {row['feature_id']}: {row['candidate_name']} "
                f"({row['ppm_error']:.3f} ppm; {row['identification_status']})\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Exact mass alone is not definitive molecular identification. Real workflows require calibration, isotope scoring, adduct logic, retention time, MS/MS evidence, blanks, quality controls, and expert review.\n")

    print("Mass spectrometry workflow complete.")

if __name__ == "__main__":
    main()
