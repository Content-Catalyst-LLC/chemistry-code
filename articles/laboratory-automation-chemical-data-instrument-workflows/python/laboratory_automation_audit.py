#!/usr/bin/env python3
"""
Synthetic laboratory automation audit workflow.

This script demonstrates:
1. Instrument run-manifest checks.
2. Required metadata completeness.
3. QC review queue generation.
4. Turnaround-time metrics.
5. Data-file provenance checks.
6. Automation audit manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
REPORT_DIR = BASE_DIR / "outputs" / "reports"
MANIFEST_DIR = BASE_DIR / "outputs" / "manifests"

REQUIRED_RUN_FIELDS = [
    "run_id",
    "sample_id",
    "sample_type",
    "instrument_id",
    "method_id",
    "scheduled_time",
    "completed_time",
    "raw_file",
    "processed_file",
    "qc_status",
]

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def parse_time(value: str):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d %H:%M")

def as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    runs = read_csv(DATA_DIR / "run_manifest.csv")
    samples = read_csv(DATA_DIR / "sample_queue.csv")
    methods = read_csv(DATA_DIR / "instrument_methods.csv")
    qc_results = read_csv(DATA_DIR / "qc_results.csv")
    data_files = read_csv(DATA_DIR / "data_files.csv")
    audit_events = read_csv(DATA_DIR / "audit_events.csv")

    method_lookup = {row["method_id"]: row for row in methods}
    files_by_run: dict[str, list[dict[str, str]]] = {}
    for row in data_files:
        files_by_run.setdefault(row["run_id"], []).append(row)

    audit_rows = []

    for row in runs:
        present_count = sum(1 for field in REQUIRED_RUN_FIELDS if row.get(field))
        completeness = present_count / len(REQUIRED_RUN_FIELDS)

        scheduled = parse_time(row["scheduled_time"])
        completed = parse_time(row["completed_time"])
        turnaround_min = None
        if scheduled and completed:
            turnaround_min = (completed - scheduled).total_seconds() / 60.0

        run_files = files_by_run.get(row["run_id"], [])
        raw_file_count = sum(1 for f in run_files if f["file_type"] == "raw")
        processed_file_count = sum(1 for f in run_files if f["file_type"] == "processed")
        missing_checksum_count = sum(1 for f in run_files if not as_bool(f["checksum_present"]))

        method = method_lookup.get(row["method_id"], {})
        expected_runtime = float(method.get("expected_runtime_min", 0) or 0)
        runtime_delta_min = None
        if turnaround_min is not None and expected_runtime:
            runtime_delta_min = turnaround_min - expected_runtime

        review_required = (
            completeness < 1.0
            or row["qc_status"] != "pass"
            or as_bool(row["exception_flag"])
            or raw_file_count == 0
            or processed_file_count == 0
            or missing_checksum_count > 0
        )

        audit_rows.append({
            "run_id": row["run_id"],
            "sample_id": row["sample_id"],
            "sample_type": row["sample_type"],
            "instrument_id": row["instrument_id"],
            "method_id": row["method_id"],
            "qc_status": row["qc_status"],
            "metadata_completeness": completeness,
            "turnaround_min": "" if turnaround_min is None else turnaround_min,
            "expected_runtime_min": expected_runtime,
            "runtime_delta_min": "" if runtime_delta_min is None else runtime_delta_min,
            "raw_file_count": raw_file_count,
            "processed_file_count": processed_file_count,
            "missing_checksum_count": missing_checksum_count,
            "review_required": review_required,
        })

    review_rows = [row for row in audit_rows if row["review_required"]]

    completed_count = sum(1 for row in runs if row["completed_time"])
    scheduled_count = len(runs)
    failed_count = sum(1 for row in runs if row["qc_status"] == "failed")
    warning_count = sum(1 for row in runs if row["qc_status"] == "warning")
    completion_fraction = completed_count / scheduled_count
    failure_fraction = failed_count / scheduled_count

    turnaround_values = [
        float(row["turnaround_min"])
        for row in audit_rows
        if row["turnaround_min"] != ""
    ]

    write_csv(
        TABLE_DIR / "automation_run_audit.csv",
        audit_rows,
        [
            "run_id",
            "sample_id",
            "sample_type",
            "instrument_id",
            "method_id",
            "qc_status",
            "metadata_completeness",
            "turnaround_min",
            "expected_runtime_min",
            "runtime_delta_min",
            "raw_file_count",
            "processed_file_count",
            "missing_checksum_count",
            "review_required",
        ],
    )

    write_csv(
        TABLE_DIR / "automation_review_queue.csv",
        review_rows,
        [
            "run_id",
            "sample_id",
            "sample_type",
            "instrument_id",
            "method_id",
            "qc_status",
            "metadata_completeness",
            "turnaround_min",
            "expected_runtime_min",
            "runtime_delta_min",
            "raw_file_count",
            "processed_file_count",
            "missing_checksum_count",
            "review_required",
        ],
    )

    manifest = {
        "article": "Laboratory Automation, Chemical Data, and Instrument Workflows",
        "data_type": "synthetic educational laboratory automation data",
        "scheduled_count": scheduled_count,
        "completed_count": completed_count,
        "failed_count": failed_count,
        "warning_count": warning_count,
        "completion_fraction": completion_fraction,
        "failure_fraction": failure_fraction,
        "mean_metadata_completeness": mean([row["metadata_completeness"] for row in audit_rows]),
        "mean_turnaround_min": mean(turnaround_values),
        "review_required_count": len(review_rows),
        "sample_count": len(samples),
        "method_count": len(methods),
        "qc_result_count": len(qc_results),
        "data_file_count": len(data_files),
        "audit_event_count": len(audit_events),
        "responsible_use": "Synthetic educational data only; not validated for regulated laboratory decisions.",
    }

    with (MANIFEST_DIR / "laboratory_automation_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "laboratory_automation_audit_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Laboratory Automation Audit Report\n\n")
        handle.write("Synthetic educational laboratory automation workflow.\n\n")
        handle.write("## Workflow Summary\n\n")
        handle.write(f"- Scheduled runs: {scheduled_count}\n")
        handle.write(f"- Completed runs: {completed_count}\n")
        handle.write(f"- Completion fraction: {completion_fraction:.3f}\n")
        handle.write(f"- Failure fraction: {failure_fraction:.3f}\n")
        handle.write(f"- Review-required runs: {len(review_rows)}\n")
        handle.write("\n## Review Queue\n\n")
        for row in review_rows:
            handle.write(
                f"- {row['run_id']} / {row['sample_id']}: "
                f"QC={row['qc_status']}, completeness={row['metadata_completeness']:.2f}, "
                f"missing checksums={row['missing_checksum_count']}\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real automated laboratories require validated LIMS, audit trails, instrument controls, quality systems, and documented exception handling.\n")

    print("Laboratory automation audit workflow complete.")

if __name__ == "__main__":
    main()
