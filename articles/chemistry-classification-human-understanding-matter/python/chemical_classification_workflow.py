#!/usr/bin/env python3
"""
Chemistry, Classification, and the Human Understanding of Matter

Synthetic educational workflow for chemical classification:
- substance-versus-mixture screening
- organic, ionic, metallic, polymer, extended-solid, and coordination classification
- evidence-weighted classification confidence
- hazard-category triage
- material-class summary

Not a real unknown-identification, regulatory, SDS, purity, or analytical validation tool.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "chemical_classification_full_stack_synthetic.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_REPORTS = ROOT / "outputs" / "reports"
OUT_MANIFESTS = ROOT / "outputs" / "manifests"

NUMERIC = {
    "components",
    "molecular_weight",
    "charge",
    "contains_metal",
    "coordination_number",
    "is_polymer",
    "network_structure",
    "organic_fraction",
    "ionic_fraction",
    "metallic_fraction",
    "crystalline_score",
    "spectral_match_score",
    "elemental_match_score",
    "thermal_signature_score",
    "hazard_indicator_score",
    "classification_confidence",
    "qc_score",
}


def parse_float(value: str) -> float:
    if value == "":
        return 0.0
    return float(value)


def load_rows() -> list[dict]:
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        rows = []
        for row in csv.DictReader(handle):
            parsed = {k: parse_float(v) if k in NUMERIC else v for k, v in row.items()}
            rows.append(parsed)
        return rows


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def classify(row: dict) -> str:
    if row["components"] > 3:
        if row["phase"] == "heterogeneous_mixture":
            return "heterogeneous_mixture"
        return "mixture_or_solution"

    if row["is_polymer"] >= 1:
        return "polymer_material"

    if row["contains_metal"] >= 1 and row["coordination_number"] >= 4 and row["functional_group"] == "coordination_complex":
        return "coordination_compound"

    if row["ionic_fraction"] >= 0.65 and row["crystalline_score"] >= 0.65:
        return "ionic_or_salt_crystal"

    if row["network_structure"] >= 1 and row["phase"] in {"crystalline_solid", "amorphous_solid"}:
        return "extended_solid_or_network_material"

    if row["organic_fraction"] >= 0.65:
        return "organic_molecular_substance"

    if row["metallic_fraction"] >= 0.40:
        return "metallic_or_intermetallic_material"

    return "molecular_or_material_record"


def evidence_score(row: dict) -> float:
    return clamp(
        0.35 * row["spectral_match_score"] +
        0.30 * row["elemental_match_score"] +
        0.20 * row["thermal_signature_score"] +
        0.15 * row["qc_score"]
    )


def classification_reliability(row: dict) -> float:
    return clamp(
        0.55 * evidence_score(row) +
        0.30 * row["classification_confidence"] +
        0.15 * row["qc_score"]
    )


def hazard_triage(row: dict) -> str:
    if row["hazard_indicator_score"] >= 0.60:
        return "higher_attention"
    if row["hazard_indicator_score"] >= 0.35:
        return "moderate_attention"
    return "lower_attention"


def enrich(row: dict) -> dict:
    assigned = classify(row)
    reliability = classification_reliability(row)
    return {
        **row,
        "assigned_class": assigned,
        "evidence_score": evidence_score(row),
        "classification_reliability": reliability,
        "hazard_triage": hazard_triage(row),
    }


def summarize(rows: list[dict], key: str) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)

    return [
        {
            key: group,
            "n": len(records),
            "mean_evidence_score": mean(r["evidence_score"] for r in records),
            "mean_classification_reliability": mean(r["classification_reliability"] for r in records),
            "mean_hazard_indicator_score": mean(r["hazard_indicator_score"] for r in records),
            "mean_qc_score": mean(r["qc_score"] for r in records),
        }
        for group, records in sorted(groups.items())
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict]) -> None:
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)
    ranked = sorted(rows, key=lambda r: r["classification_reliability"], reverse=True)

    lines = [
        "# Chemical Classification Report",
        "",
        "Synthetic educational classification of chemical records.",
        "",
        "## Highest-reliability records",
        "",
    ]

    for row in ranked[:6]:
        lines.append(
            f"- {row['sample_name']}: class={row['assigned_class']}, "
            f"reliability={row['classification_reliability']:.3f}, "
            f"evidence={row['evidence_score']:.3f}, hazard={row['hazard_triage']}"
        )

    lines.extend([
        "",
        "## Responsible-use note",
        "",
        "These outputs are synthetic and educational. They do not identify real unknowns, validate laboratory data, assign regulatory classifications, produce safety data sheets, certify purity, or substitute for expert analytical review.",
    ])

    (OUT_REPORTS / "chemical_classification_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(rows: list[dict]) -> None:
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "chemistry-classification-human-understanding-matter",
        "title": "Chemistry, Classification, and the Human Understanding of Matter",
        "records": len(rows),
        "outputs": [
            "outputs/tables/chemical_classification_indicators.csv",
            "outputs/tables/chemical_classification_class_summary.csv",
            "outputs/reports/chemical_classification_report.md"
        ],
        "responsible_use": "Synthetic educational workflow only; not unknown identification, regulatory classification, SDS generation, purity certification, or analytical validation."
    }
    (OUT_MANIFESTS / "chemical_classification_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    rows = [enrich(row) for row in load_rows()]

    write_csv(OUT_TABLES / "chemical_classification_indicators.csv", rows)
    write_csv(OUT_TABLES / "chemical_classification_class_summary.csv", summarize(rows, "assigned_class"))
    write_report(rows)
    write_manifest(rows)

    print("Chemical classification workflow complete.")
    print(f"Records: {len(rows)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
