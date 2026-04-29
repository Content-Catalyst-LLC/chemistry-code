#!/usr/bin/env python3
"""
Notebook reproducibility audit for synthetic chemical calibration data.

This script uses synthetic UV-Vis calibration records to demonstrate how
a chemical notebook workflow can preserve calibration parameters, notebook
metadata, instrument identifiers, execution order, and machine-readable
provenance outputs.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, stdev
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "synthetic_chemical_notebook_runs.csv"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
MANIFEST_DIR = BASE_DIR / "outputs" / "manifests"
REPORT_DIR = BASE_DIR / "outputs" / "reports"


@dataclass
class RunRecord:
    run_id: str
    notebook_id: str
    molecule: str
    method: str
    instrument_id: str
    environment_id: str
    concentration_mol_l: float
    absorbance: float
    temperature_k: float
    analyst: str
    random_seed: int
    execution_order: int


def read_records(path: Path) -> list[RunRecord]:
    """Read synthetic chemical notebook run records from CSV."""
    records: list[RunRecord] = []

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            records.append(
                RunRecord(
                    run_id=row["run_id"],
                    notebook_id=row["notebook_id"],
                    molecule=row["molecule"],
                    method=row["method"],
                    instrument_id=row["instrument_id"],
                    environment_id=row["environment_id"],
                    concentration_mol_l=float(row["concentration_mol_l"]),
                    absorbance=float(row["absorbance"]),
                    temperature_k=float(row["temperature_k"]),
                    analyst=row["analyst"],
                    random_seed=int(row["random_seed"]),
                    execution_order=int(row["execution_order"]),
                )
            )

    return records


def fit_linear_calibration(records: Iterable[RunRecord]) -> dict[str, float]:
    """
    Fit absorbance = intercept + slope * concentration using closed-form
    ordinary least squares for one predictor.
    """
    rows = list(records)
    x = [row.concentration_mol_l for row in rows]
    y = [row.absorbance for row in rows]

    x_bar = mean(x)
    y_bar = mean(y)

    numerator = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    denominator = sum((xi - x_bar) ** 2 for xi in x)

    slope = numerator / denominator
    intercept = y_bar - slope * x_bar

    predicted = [intercept + slope * xi for xi in x]
    residuals = [yi - yhat for yi, yhat in zip(y, predicted)]

    ss_residual = sum(residual ** 2 for residual in residuals)
    ss_total = sum((yi - y_bar) ** 2 for yi in y)
    r_squared = 1.0 - ss_residual / ss_total

    return {
        "slope_absorbance_per_mol_l": slope,
        "intercept_absorbance": intercept,
        "r_squared": r_squared,
        "residual_standard_deviation": stdev(residuals),
    }


def summarize_by_notebook(records: Iterable[RunRecord]) -> list[dict[str, object]]:
    """Summarize reproducibility-relevant run metadata by notebook identifier."""
    groups: dict[str, list[RunRecord]] = defaultdict(list)

    for record in records:
        groups[record.notebook_id].append(record)

    summaries: list[dict[str, object]] = []

    for notebook_id, rows in sorted(groups.items()):
        absorbances = [row.absorbance for row in rows]
        temperatures = [row.temperature_k for row in rows]

        summaries.append(
            {
                "notebook_id": notebook_id,
                "row_count": len(rows),
                "molecule": sorted({row.molecule for row in rows})[0],
                "method": sorted({row.method for row in rows})[0],
                "instrument_ids": sorted({row.instrument_id for row in rows}),
                "environment_ids": sorted({row.environment_id for row in rows}),
                "analysts": sorted({row.analyst for row in rows}),
                "mean_absorbance": mean(absorbances),
                "sd_absorbance": stdev(absorbances),
                "mean_temperature_k": mean(temperatures),
                "random_seeds": sorted({row.random_seed for row in rows}),
            }
        )

    return summaries


def write_summary_csv(path: Path, summaries: list[dict[str, object]]) -> None:
    """Write a flat CSV summary suitable for audit tables."""
    fieldnames = [
        "notebook_id",
        "row_count",
        "molecule",
        "method",
        "instrument_ids",
        "environment_ids",
        "analysts",
        "mean_absorbance",
        "sd_absorbance",
        "mean_temperature_k",
        "random_seeds",
    ]

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for row in summaries:
            flat_row = dict(row)

            for key in ["instrument_ids", "environment_ids", "analysts", "random_seeds"]:
                flat_row[key] = ";".join(str(item) for item in flat_row[key])

            writer.writerow(flat_row)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    records = read_records(DATA_PATH)
    calibration = fit_linear_calibration(records)
    notebook_summaries = summarize_by_notebook(records)

    write_summary_csv(TABLE_DIR / "notebook_reproducibility_summary.csv", notebook_summaries)

    manifest = {
        "article": "Computational Notebooks and Reproducible Chemical Research",
        "dataset": str(DATA_PATH.relative_to(BASE_DIR)),
        "dataset_type": "synthetic educational UV-Vis calibration records",
        "record_count": len(records),
        "notebook_count": len({record.notebook_id for record in records}),
        "environment_count": len({record.environment_id for record in records}),
        "calibration_model": "absorbance = intercept + slope * concentration_mol_l",
        "calibration": calibration,
        "responsible_use": "Synthetic data only; not for regulatory, safety, clinical, or environmental-compliance decisions.",
    }

    with (MANIFEST_DIR / "reproducibility_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "notebook_audit_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Notebook Reproducibility Audit Report\n\n")
        handle.write("This report summarizes a synthetic chemical calibration notebook workflow.\n\n")
        handle.write("## Calibration Model\n\n")

        for key, value in calibration.items():
            handle.write(f"- **{key}:** {value:.8g}\n")

        handle.write("\n## Notebook Summaries\n\n")

        for row in notebook_summaries:
            handle.write(
                f"- `{row['notebook_id']}`: {row['row_count']} rows, "
                f"instruments {row['instrument_ids']}, "
                f"environments {row['environment_ids']}\n"
            )

    print("Wrote reproducibility tables, manifest, and audit report.")


if __name__ == "__main__":
    main()
