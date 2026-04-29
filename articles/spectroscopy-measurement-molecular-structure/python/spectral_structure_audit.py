#!/usr/bin/env python3
"""
Synthetic spectroscopy workflow for molecular-structure clues.

This script demonstrates:
1. IR peak educational region assignment.
2. Photon-energy conversion from wavenumber.
3. UV-visible calibration from synthetic standards.
4. NMR signal table summarization.
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

PLANCK_J_S = 6.62607015e-34
LIGHT_M_S = 299792458
AVOGADRO = 6.02214076e23

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def assign_ir_region(wavenumber: float) -> str:
    if 3200 <= wavenumber <= 3600:
        return "possible O-H or N-H stretching region"
    if 3000 <= wavenumber <= 3100:
        return "possible aromatic or alkene C-H stretching region"
    if 2850 <= wavenumber < 3000:
        return "possible aliphatic C-H stretching region"
    if 1650 <= wavenumber <= 1800:
        return "possible carbonyl stretching region"
    if 1500 <= wavenumber < 1650:
        return "possible C=C or aromatic ring region"
    if 1000 <= wavenumber <= 1300:
        return "possible C-O, C-N, or fingerprint-region feature"
    if 650 <= wavenumber <= 900:
        return "possible aromatic C-H out-of-plane region"
    return "unassigned educational region"

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

def process_ir() -> list[dict[str, object]]:
    rows = read_csv(DATA_DIR / "ir_peaks.csv")
    processed = []

    for row in rows:
        wavenumber = float(row["wavenumber_cm_minus_1"])
        photon_energy_j = PLANCK_J_S * LIGHT_M_S * wavenumber * 100.0
        photon_energy_kj_mol = photon_energy_j * AVOGADRO / 1000.0

        processed.append({
            "peak_id": row["peak_id"],
            "sample_id": row["sample_id"],
            "wavenumber_cm_minus_1": wavenumber,
            "relative_intensity": float(row["relative_intensity"]),
            "educational_assignment": assign_ir_region(wavenumber),
            "photon_energy_kj_per_mol": photon_energy_kj_mol,
        })

    return processed

def process_uvvis() -> dict[str, object]:
    rows = read_csv(DATA_DIR / "uvvis_calibration.csv")
    standards = [r for r in rows if r["standard_id"].startswith("std") or r["standard_id"] == "blank"]
    unknowns = [r for r in rows if r["standard_id"].startswith("unknown")]

    x = [float(r["concentration_mol_l"]) for r in standards]
    y = [float(r["absorbance"]) for r in standards]
    model = fit_linear_model(x, y)

    unknown_estimates = []

    for row in unknowns:
        absorbance = float(row["absorbance"])
        estimated_concentration = (absorbance - model["intercept"]) / model["slope"]
        unknown_estimates.append({
            "sample_id": row["standard_id"],
            "absorbance": absorbance,
            "estimated_concentration_mol_l": estimated_concentration,
        })

    return {
        "model": model,
        "unknown_estimates": unknown_estimates,
        "mean_unknown_concentration_mol_l": mean([r["estimated_concentration_mol_l"] for r in unknown_estimates]),
    }

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    ir_processed = process_ir()
    uvvis_result = process_uvvis()
    nmr_rows = read_csv(DATA_DIR / "nmr_signals.csv")
    metadata_rows = read_csv(DATA_DIR / "spectral_metadata.csv")

    write_csv(
        TABLE_DIR / "ir_peak_assignments.csv",
        ir_processed,
        [
            "peak_id",
            "sample_id",
            "wavenumber_cm_minus_1",
            "relative_intensity",
            "educational_assignment",
            "photon_energy_kj_per_mol",
        ],
    )

    write_csv(
        TABLE_DIR / "uvvis_unknown_estimates.csv",
        uvvis_result["unknown_estimates"],
        ["sample_id", "absorbance", "estimated_concentration_mol_l"],
    )

    manifest = {
        "article": "Spectroscopy and the Measurement of Molecular Structure",
        "data_type": "synthetic educational spectroscopy data",
        "ir_peak_count": len(ir_processed),
        "nmr_signal_count": len(nmr_rows),
        "metadata_record_count": len(metadata_rows),
        "uvvis_calibration": uvvis_result["model"],
        "mean_unknown_concentration_mol_l": uvvis_result["mean_unknown_concentration_mol_l"],
        "responsible_use": "Synthetic educational data only; not validated for laboratory, clinical, forensic, environmental, industrial, or regulatory use.",
    }

    with (MANIFEST_DIR / "spectroscopy_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "spectroscopy_audit_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Spectroscopy Audit Report\n\n")
        handle.write("Synthetic educational spectroscopy workflow.\n\n")
        handle.write("## UV-Visible Calibration\n\n")
        for key, value in uvvis_result["model"].items():
            handle.write(f"- **{key}:** {value:.8g}\n")
        handle.write("\n## IR Structural Clues\n\n")
        for row in ir_processed:
            handle.write(
                f"- {row['sample_id']} peak at {row['wavenumber_cm_minus_1']:.0f} cm^-1: "
                f"{row['educational_assignment']}\n"
            )

    print("Spectroscopy workflow complete.")

if __name__ == "__main__":
    main()
