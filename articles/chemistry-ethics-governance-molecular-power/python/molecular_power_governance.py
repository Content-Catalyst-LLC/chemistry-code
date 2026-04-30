#!/usr/bin/env python3
"""
Chemistry, Ethics, and the Governance of Molecular Power

Synthetic educational workflow for governance-oriented chemical screening:
- risk
- justice-weighted risk
- governance gap
- stewardship score
- transparency/data confidence
- dual-use concern flag
- responsible innovation score

Not a legal, regulatory, toxicological, safety, security, exposure, or product-approval tool.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "molecular_power_governance_synthetic.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_REPORTS = ROOT / "outputs" / "reports"
OUT_MANIFESTS = ROOT / "outputs" / "manifests"

NUMERIC = {
    "benefit_score",
    "hazard_score",
    "exposure_potential",
    "vulnerability_factor",
    "persistence_score",
    "irreversibility_score",
    "inequality_burden_score",
    "worker_exposure_score",
    "dual_use_concern",
    "transparency_score",
    "monitoring_score",
    "alternatives_score",
    "stewardship_score",
    "governance_strength",
    "data_completeness",
    "qc_score",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def parse_row(row: dict) -> dict:
    return {k: float(v) if k in NUMERIC else v for k, v in row.items()}


def load_rows() -> list[dict]:
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        return [parse_row(row) for row in csv.DictReader(handle)]


def chemical_risk(row: dict) -> float:
    baseline = row["hazard_score"] * row["exposure_potential"] * row["vulnerability_factor"]
    persistence = 0.5 * row["persistence_score"] + 0.5 * row["irreversibility_score"]
    return clamp(0.72 * baseline + 0.28 * persistence)


def justice_weighted_risk(row: dict) -> float:
    risk = chemical_risk(row)
    inequality = row["inequality_burden_score"]
    worker = row["worker_exposure_score"]
    return clamp(risk * (1.0 + 0.50 * inequality + 0.35 * worker))


def governance_gap(row: dict) -> float:
    return clamp(justice_weighted_risk(row) * (1.0 - row["governance_strength"]))


def transparency_confidence(row: dict) -> float:
    return clamp(
        0.40 * row["transparency_score"] +
        0.30 * row["data_completeness"] +
        0.20 * row["monitoring_score"] +
        0.10 * row["qc_score"]
    )


def stewardship_capacity(row: dict) -> float:
    return clamp(
        0.35 * row["stewardship_score"] +
        0.25 * row["governance_strength"] +
        0.20 * row["monitoring_score"] +
        0.20 * row["alternatives_score"]
    )


def responsible_innovation_score(row: dict) -> float:
    benefit = row["benefit_score"]
    stewardship = stewardship_capacity(row)
    transparency = transparency_confidence(row)
    alternatives = row["alternatives_score"]
    jrisk = justice_weighted_risk(row)
    dual = row["dual_use_concern"]
    gap = governance_gap(row)

    return clamp(
        0.26 * benefit +
        0.22 * stewardship +
        0.16 * transparency +
        0.12 * alternatives -
        0.14 * jrisk -
        0.06 * dual -
        0.04 * gap
    )


def governance_flag(row: dict) -> str:
    if row["dual_use_concern"] >= 0.80:
        return "restricted_or_high_dual_use_governance_attention"
    if row["governance_gap"] >= 0.40:
        return "high_governance_gap"
    if row["justice_weighted_risk"] >= 0.55:
        return "high_justice_weighted_risk"
    if row["responsible_innovation_score"] >= 0.65:
        return "stronger_responsible_innovation_profile"
    return "monitor_and_improve_governance"


def enrich(row: dict) -> dict:
    enriched = {
        **row,
        "chemical_risk": chemical_risk(row),
        "justice_weighted_risk": justice_weighted_risk(row),
        "governance_gap": governance_gap(row),
        "transparency_confidence": transparency_confidence(row),
        "stewardship_capacity": stewardship_capacity(row),
        "responsible_innovation_score": responsible_innovation_score(row),
    }
    enriched["governance_flag"] = governance_flag(enriched)
    return enriched


def summarize(rows: list[dict], key: str) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)

    return [
        {
            key: group,
            "n": len(records),
            "mean_benefit_score": mean(r["benefit_score"] for r in records),
            "mean_chemical_risk": mean(r["chemical_risk"] for r in records),
            "mean_justice_weighted_risk": mean(r["justice_weighted_risk"] for r in records),
            "mean_governance_gap": mean(r["governance_gap"] for r in records),
            "mean_responsible_innovation_score": mean(r["responsible_innovation_score"] for r in records),
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
    ranked_gap = sorted(rows, key=lambda r: r["governance_gap"], reverse=True)
    ranked_score = sorted(rows, key=lambda r: r["responsible_innovation_score"], reverse=True)

    lines = [
        "# Molecular Power Governance Screening Report",
        "",
        "Synthetic educational screening of chemical governance indicators.",
        "",
        "## Highest governance gaps",
        "",
    ]

    for row in ranked_gap[:4]:
        lines.append(
            f"- {row['use_context']}: gap={row['governance_gap']:.3f}, "
            f"justice risk={row['justice_weighted_risk']:.3f}, flag={row['governance_flag']}"
        )

    lines.extend(["", "## Strongest responsible-innovation profiles", ""])

    for row in ranked_score[:4]:
        lines.append(
            f"- {row['use_context']}: score={row['responsible_innovation_score']:.3f}, "
            f"benefit={row['benefit_score']:.3f}, stewardship={row['stewardship_capacity']:.3f}"
        )

    lines.extend([
        "",
        "## Responsible-use note",
        "",
        "These outputs are synthetic and educational. They are not legal, regulatory, toxicological, security, safety, exposure, or product-approval determinations.",
    ])

    (OUT_REPORTS / "molecular_power_governance_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(rows: list[dict]) -> None:
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "chemistry-ethics-governance-molecular-power",
        "title": "Chemistry, Ethics, and the Governance of Molecular Power",
        "records": len(rows),
        "outputs": [
            "outputs/tables/molecular_power_governance_indicators.csv",
            "outputs/tables/molecular_power_domain_summary.csv",
            "outputs/reports/molecular_power_governance_report.md"
        ],
        "responsible_use": "Synthetic educational workflow only; not legal, regulatory, toxicological, safety, security, exposure, or product-approval support."
    }
    (OUT_MANIFESTS / "molecular_power_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    rows = [enrich(row) for row in load_rows()]

    write_csv(OUT_TABLES / "molecular_power_governance_indicators.csv", rows)
    write_csv(OUT_TABLES / "molecular_power_domain_summary.csv", summarize(rows, "chemical_domain"))
    write_report(rows)
    write_manifest(rows)

    print("Molecular power governance workflow complete.")
    print(f"Records: {len(rows)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
