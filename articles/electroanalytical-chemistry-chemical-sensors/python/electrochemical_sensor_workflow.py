#!/usr/bin/env python3
"""
Synthetic electroanalytical chemistry workflow for chemical sensor validation.

This script demonstrates:
1. Amperometric calibration.
2. Detection-limit estimation.
3. Unknown concentration estimation.
4. Sensor drift summary.
5. Potentiometric Nernst-slope summary.
6. Interference testing.
7. Provenance-manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
import math
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
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "residual_standard_deviation": stdev(residuals),
    }

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    calibration = read_csv(DATA_DIR / "sensor_calibration.csv")
    unknowns = read_csv(DATA_DIR / "unknown_sensor_samples.csv")
    drift = read_csv(DATA_DIR / "sensor_drift.csv")
    potentiometry = read_csv(DATA_DIR / "potentiometric_response.csv")
    voltammetry = read_csv(DATA_DIR / "voltammetric_peaks.csv")
    interferences = read_csv(DATA_DIR / "interference_tests.csv")
    metadata_rows = read_csv(DATA_DIR / "electrochemical_metadata.csv")

    x = [float(row["concentration_uM"]) for row in calibration]
    y = [float(row["current_uA"]) for row in calibration]
    calibration_model = fit_linear_model(x, y)

    blank_currents = [
        float(row["current_uA"])
        for row in calibration
        if float(row["concentration_uM"]) == 0.0
    ]
    blank_sd = stdev(blank_currents)
    lod_uM = 3.0 * blank_sd / calibration_model["slope"]

    unknown_estimates = []
    for row in unknowns:
        current = float(row["current_uA"])
        estimated_concentration = (
            current - calibration_model["intercept"]
        ) / calibration_model["slope"]
        unknown_estimates.append({
            "sample_id": row["sample_id"],
            "replicate_id": row["replicate_id"],
            "current_uA": current,
            "estimated_concentration_uM": estimated_concentration,
            "electrode_id": row["electrode_id"],
            "matrix": row["matrix"],
        })

    summary_by_sample = {}
    for row in unknown_estimates:
        summary_by_sample.setdefault(row["sample_id"], []).append(row)

    unknown_summary = []
    for sample_id, rows in sorted(summary_by_sample.items()):
        concentrations = [row["estimated_concentration_uM"] for row in rows]
        currents = [row["current_uA"] for row in rows]
        unknown_summary.append({
            "sample_id": sample_id,
            "mean_current_uA": mean(currents),
            "sd_current_uA": stdev(currents),
            "mean_concentration_uM": mean(concentrations),
            "sd_concentration_uM": stdev(concentrations),
            "replicate_count": len(rows),
        })

    drift_times = [float(row["time_min"]) for row in drift]
    drift_currents = [float(row["current_uA"]) for row in drift]
    drift_model = fit_linear_model(drift_times, drift_currents)
    percent_change = 100.0 * (drift_currents[-1] - drift_currents[0]) / drift_currents[0]

    drift_summary = [{
        "drift_slope_uA_per_min": drift_model["slope"],
        "initial_current_uA": drift_currents[0],
        "final_current_uA": drift_currents[-1],
        "percent_change": percent_change,
    }]

    p_x = [math.log10(float(row["ion_activity"])) for row in potentiometry]
    p_y = [float(row["potential_mV"]) for row in potentiometry]
    nernst_fit = fit_linear_model(p_x, p_y)

    high_interference_rows = []
    for row in interferences:
        change = float(row["response_change_percent"])
        if abs(change) >= 5.0:
            high_interference_rows.append({
                "test_id": row["test_id"],
                "interferent": row["interferent"],
                "interferent_concentration_uM": float(row["interferent_concentration_uM"]),
                "response_change_percent": change,
                "interpretation": "potentially important interference in synthetic test",
            })

    write_csv(
        TABLE_DIR / "sensor_unknown_estimates.csv",
        unknown_estimates,
        ["sample_id", "replicate_id", "current_uA", "estimated_concentration_uM", "electrode_id", "matrix"],
    )

    write_csv(
        TABLE_DIR / "sensor_unknown_summary.csv",
        unknown_summary,
        ["sample_id", "mean_current_uA", "sd_current_uA", "mean_concentration_uM", "sd_concentration_uM", "replicate_count"],
    )

    write_csv(
        TABLE_DIR / "sensor_drift_summary.csv",
        drift_summary,
        ["drift_slope_uA_per_min", "initial_current_uA", "final_current_uA", "percent_change"],
    )

    write_csv(
        TABLE_DIR / "interference_flags.csv",
        high_interference_rows,
        ["test_id", "interferent", "interferent_concentration_uM", "response_change_percent", "interpretation"],
    )

    manifest = {
        "article": "Electroanalytical Chemistry and Chemical Sensors",
        "data_type": "synthetic educational electroanalytical data",
        "calibration_model": {
            "model": "current_uA = intercept + sensitivity * concentration_uM",
            "sensitivity_uA_per_uM": calibration_model["slope"],
            "intercept_uA": calibration_model["intercept"],
            "r_squared": calibration_model["r_squared"],
            "blank_standard_deviation_uA": blank_sd,
            "limit_of_detection_uM": lod_uM,
        },
        "nernst_like_potential_slope_mV_per_decade": nernst_fit["slope"],
        "unknown_sample_count": len(unknown_summary),
        "drift_percent_change": percent_change,
        "voltammetric_peak_count": len(voltammetry),
        "interference_flag_count": len(high_interference_rows),
        "metadata_record_count": len(metadata_rows),
        "responsible_use": "Synthetic educational data only; not validated for clinical, environmental, forensic, regulatory, or safety-critical use.",
    }

    with (MANIFEST_DIR / "electrochemical_sensor_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "electrochemical_sensor_audit_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Electrochemical Sensor Audit Report\n\n")
        handle.write("Synthetic educational electroanalytical chemistry workflow.\n\n")
        handle.write("## Amperometric Calibration\n\n")
        handle.write(f"- Sensitivity: {calibration_model['slope']:.8g} uA/uM\n")
        handle.write(f"- Intercept: {calibration_model['intercept']:.8g} uA\n")
        handle.write(f"- R-squared: {calibration_model['r_squared']:.8g}\n")
        handle.write(f"- Estimated LOD: {lod_uM:.8g} uM\n")
        handle.write("\n## Drift\n\n")
        handle.write(f"- Percent change over drift check: {percent_change:.4g}%\n")
        handle.write("\n## Interference Flags\n\n")
        if high_interference_rows:
            for row in high_interference_rows:
                handle.write(f"- {row['interferent']}: {row['response_change_percent']}% response change\n")
        else:
            handle.write("- No synthetic interference exceeded the flag threshold.\n")
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real sensors require selectivity testing, matrix validation, drift evaluation, uncertainty analysis, and comparison with appropriate reference methods where relevant.\n")

    print("Electrochemical sensor workflow complete.")

if __name__ == "__main__":
    main()
