#!/usr/bin/env python3
"""
Advanced toxicology and exposure-science workflow.

Article:
Toxicology, Exposure, and Chemical Risk

This script uses synthetic toxicology and exposure records to calculate:

- route-specific chronic daily intake
- absorbed dose
- hazard quotient
- target-system hazard index
- margin of exposure
- cancer-risk proxy
- vulnerability-adjusted hazard
- evidence-weighted risk index
- mixture burden by target system and mixture group
- Monte Carlo uncertainty intervals
- exposure-reduction scenarios
- body-weight vulnerability scenarios

This is educational scaffolding only. It is not a regulatory compliance tool,
public-health advisory, clinical system, causation analysis, legal instrument,
cleanup determination, or occupational safety determination.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "toxicology_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "concentration",
    "reference_dose_mg_kg_day",
    "slope_factor_per_mg_kg_day",
    "point_of_departure_mg_kg_day",
    "intake_rate",
    "body_weight_kg",
    "exposure_frequency_days_year",
    "exposure_duration_years",
    "averaging_time_days",
    "absorption_fraction",
    "exposure_quality_score",
    "vulnerability_factor",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp value to interval."""
    return max(low, min(high, value))


def parse_value(key: str, value: str):
    """Parse numeric fields from CSV."""
    if key in NUMERIC_FIELDS:
        return float(value)
    return value


def stable_seed(text: str) -> int:
    """Generate stable deterministic seed from string."""
    total = 0
    for index, char in enumerate(text):
        total += (index + 1) * ord(char)
    return total % 100000


def load_rows(path: Path = DATA_FILE) -> list[dict]:
    """Load synthetic exposure records."""
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [
            {key: parse_value(key, value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def concentration_to_mg_per_unit(row: dict) -> float:
    """
    Convert concentration to route-compatible units.

    Supported synthetic units:
    - mg_L for water
    - mg_m3 for air
    - mg_kg for food, soil, or dust
    """
    return row["concentration"]


def chronic_daily_intake(row: dict) -> float:
    """
    Simplified chronic daily intake.

    Generalized expression:
    CDI = C * IR * EF * ED / (BW * AT)

    Units are synthetic and route-compatible in this teaching dataset.
    """
    concentration = concentration_to_mg_per_unit(row)

    return (
        concentration
        * row["intake_rate"]
        * row["exposure_frequency_days_year"]
        * row["exposure_duration_years"]
    ) / (
        row["body_weight_kg"]
        * row["averaging_time_days"]
    )


def absorbed_dose(row: dict) -> float:
    """Estimate absorbed dose by applying absorption fraction."""
    return chronic_daily_intake(row) * row["absorption_fraction"]


def hazard_quotient(row: dict) -> float:
    """Calculate noncancer hazard quotient."""
    rfd = row["reference_dose_mg_kg_day"]
    if rfd <= 0:
        return 0.0
    return absorbed_dose(row) / rfd


def margin_of_exposure(row: dict) -> float:
    """Calculate margin of exposure from point of departure and absorbed dose."""
    dose = absorbed_dose(row)
    if dose <= 0:
        return float("inf")
    return row["point_of_departure_mg_kg_day"] / dose


def cancer_risk_proxy(row: dict) -> float:
    """Calculate simplified cancer risk proxy."""
    slope_factor = row["slope_factor_per_mg_kg_day"]
    if slope_factor <= 0:
        return 0.0
    return absorbed_dose(row) * slope_factor


def vulnerability_adjusted_hazard(row: dict) -> float:
    """Apply vulnerability factor to hazard quotient."""
    return hazard_quotient(row) * row["vulnerability_factor"]


def evidence_weighted_risk_index(row: dict) -> float:
    """
    Composite screening index.

    Components:
    - hazard quotient
    - cancer-risk proxy
    - vulnerability
    - lower evidence quality
    """
    hq_component = clamp(math.log1p(hazard_quotient(row)) / math.log(11.0))
    cancer_component = clamp(cancer_risk_proxy(row) / 1e-4)
    vulnerability_component = clamp((row["vulnerability_factor"] - 1.0) / 1.0)
    uncertainty_component = 1.0 - row["exposure_quality_score"]

    return clamp(
        0.45 * hq_component
        + 0.25 * cancer_component
        + 0.20 * vulnerability_component
        + 0.10 * uncertainty_component
    )


def attention_flag(row: dict) -> str:
    """Classify synthetic screening concern."""
    hq = hazard_quotient(row)
    cancer = cancer_risk_proxy(row)
    index = evidence_weighted_risk_index(row)

    if hq >= 1.0 or cancer >= 1e-4 or index >= 0.65:
        return "high_attention"
    if hq >= 0.3 or cancer >= 1e-5 or index >= 0.45:
        return "moderate_attention"
    return "monitor"


def monte_carlo_uncertainty(row: dict, draws: int = 1000) -> dict:
    """
    Simple Monte Carlo uncertainty for concentration, intake, body weight,
    and reference dose.

    Educational only; not a validated probabilistic risk assessment.
    """
    rng = random.Random(stable_seed(row["record_id"]))

    hq_values = []
    cancer_values = []

    for _ in range(draws):
        simulated = dict(row)
        concentration_sigma = 0.10 + (1.0 - row["exposure_quality_score"]) * 0.40
        intake_sigma = 0.20
        body_weight_sigma = 0.10
        tox_sigma = 0.35

        simulated["concentration"] = max(0.0, row["concentration"] * rng.lognormvariate(0.0, concentration_sigma))
        simulated["intake_rate"] = max(0.000001, row["intake_rate"] * rng.lognormvariate(0.0, intake_sigma))
        simulated["body_weight_kg"] = max(1.0, row["body_weight_kg"] * rng.lognormvariate(0.0, body_weight_sigma))
        simulated["reference_dose_mg_kg_day"] = max(1e-12, row["reference_dose_mg_kg_day"] * rng.lognormvariate(0.0, tox_sigma))

        hq_values.append(hazard_quotient(simulated))
        cancer_values.append(cancer_risk_proxy(simulated))

    hq_values.sort()
    cancer_values.sort()

    def percentile(values: list[float], p: float) -> float:
        index = int(round((p / 100.0) * (len(values) - 1)))
        return values[index]

    return {
        "mc_hq_p05": percentile(hq_values, 5),
        "mc_hq_p50": percentile(hq_values, 50),
        "mc_hq_p95": percentile(hq_values, 95),
        "mc_cancer_risk_p05": percentile(cancer_values, 5),
        "mc_cancer_risk_p50": percentile(cancer_values, 50),
        "mc_cancer_risk_p95": percentile(cancer_values, 95),
        "mc_probability_hq_above_1": sum(value >= 1.0 for value in hq_values) / draws,
        "mc_draws": draws,
    }


def enrich_row(row: dict) -> dict:
    """Add toxicology indicators."""
    mc = monte_carlo_uncertainty(row)

    return {
        **row,
        "chronic_daily_intake_mg_kg_day": chronic_daily_intake(row),
        "absorbed_dose_mg_kg_day": absorbed_dose(row),
        "hazard_quotient": hazard_quotient(row),
        "vulnerability_adjusted_hazard": vulnerability_adjusted_hazard(row),
        "margin_of_exposure": margin_of_exposure(row),
        "cancer_risk_proxy": cancer_risk_proxy(row),
        "evidence_weighted_risk_index": evidence_weighted_risk_index(row),
        **mc,
        "attention_flag": attention_flag(row),
    }


def summarize_hazard_index(rows: list[dict], key: str) -> list[dict]:
    """Summarize hazard index by target system or mixture group."""
    grouped: dict[str, list[dict]] = {}

    for row in rows:
        grouped.setdefault(row[key], []).append(row)

    summaries = []

    for group, records in sorted(grouped.items()):
        summaries.append(
            {
                key: group,
                "n": len(records),
                "hazard_index": sum(row["hazard_quotient"] for row in records),
                "vulnerability_adjusted_hazard_index": sum(row["vulnerability_adjusted_hazard"] for row in records),
                "mean_evidence_weighted_risk_index": mean(row["evidence_weighted_risk_index"] for row in records),
                "max_cancer_risk_proxy": max(row["cancer_risk_proxy"] for row in records),
                "high_attention_count": sum(row["attention_flag"] == "high_attention" for row in records),
            }
        )

    return summaries


def build_exposure_reduction_scenarios(base_row: dict) -> list[dict]:
    """Build concentration-reduction scenarios."""
    rows = []

    for reduction_percent in range(0, 96, 5):
        modeled = dict(base_row)
        modeled["concentration"] = base_row["concentration"] * (1.0 - reduction_percent / 100.0)

        rows.append(
            {
                "scenario": "exposure_reduction",
                "chemical": base_row["chemical"],
                "route": base_row["route"],
                "reduction_percent": reduction_percent,
                "modeled_concentration": modeled["concentration"],
                "modeled_hazard_quotient": hazard_quotient(modeled),
                "modeled_cancer_risk_proxy": cancer_risk_proxy(modeled),
                "modeled_evidence_weighted_risk_index": evidence_weighted_risk_index(modeled),
            }
        )

    return rows


def build_body_weight_vulnerability_scenarios(base_row: dict) -> list[dict]:
    """Build body-weight and vulnerability scenario grid."""
    rows = []

    body_weights = [10, 15, 20, 50, 70, 90]
    vulnerability_factors = [1.0, 1.25, 1.5, 2.0]

    for body_weight in body_weights:
        for vulnerability in vulnerability_factors:
            modeled = dict(base_row)
            modeled["body_weight_kg"] = body_weight
            modeled["vulnerability_factor"] = vulnerability

            rows.append(
                {
                    "scenario": "body_weight_vulnerability",
                    "chemical": base_row["chemical"],
                    "body_weight_kg": body_weight,
                    "vulnerability_factor": vulnerability,
                    "modeled_hazard_quotient": hazard_quotient(modeled),
                    "modeled_vulnerability_adjusted_hazard": vulnerability_adjusted_hazard(modeled),
                }
            )

    return rows


def build_mixture_scenarios(rows: list[dict]) -> list[dict]:
    """Build mixture group contribution table."""
    output = []

    mixture_groups = sorted(set(row["mixture_group"] for row in rows))

    for group in mixture_groups:
        group_rows = [row for row in rows if row["mixture_group"] == group]
        total_hq = sum(row["hazard_quotient"] for row in group_rows)

        for row in group_rows:
            contribution = row["hazard_quotient"] / total_hq if total_hq > 0 else 0.0
            output.append(
                {
                    "scenario": "mixture_contribution",
                    "mixture_group": group,
                    "chemical": row["chemical"],
                    "hazard_quotient": row["hazard_quotient"],
                    "group_hazard_index": total_hq,
                    "fractional_hazard_contribution": contribution,
                }
            )

    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write CSV with union field names."""
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict], target_summary: list[dict], mixture_summary: list[dict]) -> None:
    """Write Markdown report."""
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    high = [row for row in rows if row["attention_flag"] == "high_attention"]
    moderate = [row for row in rows if row["attention_flag"] == "moderate_attention"]

    lines = [
        "# Advanced Toxicology and Exposure Report",
        "",
        "Synthetic educational toxicology and exposure-science summary.",
        "",
        f"Records: {len(rows)}",
        f"High attention records: {len(high)}",
        f"Moderate attention records: {len(moderate)}",
        "",
        "## High attention records",
        "",
    ]

    for row in high:
        lines.append(
            f"- {row['chemical']} via {row['route']} in {row['medium']}: "
            f"HQ={row['hazard_quotient']:.3f}, "
            f"vulnerability-adjusted HQ={row['vulnerability_adjusted_hazard']:.3f}, "
            f"MOE={row['margin_of_exposure']:.2f}, "
            f"cancer-risk proxy={row['cancer_risk_proxy']:.3e}, "
            f"MC P(HQ>=1)={row['mc_probability_hq_above_1']:.2f}"
        )

    lines.extend(["", "## Target-system hazard indices", ""])

    for row in target_summary:
        lines.append(
            f"- {row['target_system']}: "
            f"HI={row['hazard_index']:.3f}, "
            f"vulnerability-adjusted HI={row['vulnerability_adjusted_hazard_index']:.3f}, "
            f"high attention count={row['high_attention_count']}"
        )

    lines.extend(["", "## Responsible-use note", ""])
    lines.append(
        "These outputs are synthetic and educational. They are not regulatory findings, public-health advisories, clinical interpretations, causation determinations, cleanup decisions, legal evidence, or operational monitoring products."
    )

    (OUT_REPORTS / "advanced_toxicology_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(rows, target_summary, mixture_summary, exposure_scenarios, vulnerability_scenarios, mixture_scenarios) -> None:
    """Write provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "toxicology-exposure-chemical-risk",
        "title": "Toxicology, Exposure, and Chemical Risk",
        "advanced_layer": True,
        "synthetic_records": len(rows),
        "target_system_summary_rows": len(target_summary),
        "mixture_group_summary_rows": len(mixture_summary),
        "exposure_reduction_scenario_rows": len(exposure_scenarios),
        "body_weight_vulnerability_scenario_rows": len(vulnerability_scenarios),
        "mixture_contribution_rows": len(mixture_scenarios),
        "outputs": [
            "advanced/outputs/tables/advanced_toxicology_indicators.csv",
            "advanced/outputs/tables/advanced_target_system_hazard_index.csv",
            "advanced/outputs/tables/advanced_mixture_group_hazard_index.csv",
            "advanced/outputs/tables/advanced_exposure_reduction_scenarios.csv",
            "advanced/outputs/tables/advanced_body_weight_vulnerability_scenarios.csv",
            "advanced/outputs/tables/advanced_mixture_contribution_scenarios.csv",
            "advanced/outputs/reports/advanced_toxicology_report.md",
        ],
        "responsible_use": "Synthetic educational toxicology workflow only; not for regulatory, clinical, public-health, legal, occupational, cleanup, or operational decisions."
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = [enrich_row(row) for row in load_rows()]
    target_summary = summarize_hazard_index(rows, "target_system")
    mixture_summary = summarize_hazard_index(rows, "mixture_group")

    arsenic = next(row for row in rows if row["chemical"] == "arsenic")
    lead = next(row for row in rows if row["chemical"] == "lead")

    exposure_scenarios = build_exposure_reduction_scenarios(arsenic)
    vulnerability_scenarios = build_body_weight_vulnerability_scenarios(lead)
    mixture_scenarios = build_mixture_scenarios(rows)

    write_csv(OUT_TABLES / "advanced_toxicology_indicators.csv", rows)
    write_csv(OUT_TABLES / "advanced_target_system_hazard_index.csv", target_summary)
    write_csv(OUT_TABLES / "advanced_mixture_group_hazard_index.csv", mixture_summary)
    write_csv(OUT_TABLES / "advanced_exposure_reduction_scenarios.csv", exposure_scenarios)
    write_csv(OUT_TABLES / "advanced_body_weight_vulnerability_scenarios.csv", vulnerability_scenarios)
    write_csv(OUT_TABLES / "advanced_mixture_contribution_scenarios.csv", mixture_scenarios)

    write_report(rows, target_summary, mixture_summary)
    write_manifest(rows, target_summary, mixture_summary, exposure_scenarios, vulnerability_scenarios, mixture_scenarios)

    print("Advanced toxicology workflow complete.")
    print(f"Records: {len(rows)}")
    print(f"Target-system summaries: {len(target_summary)}")
    print(f"Mixture summaries: {len(mixture_summary)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
