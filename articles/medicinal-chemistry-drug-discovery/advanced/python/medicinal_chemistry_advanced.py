#!/usr/bin/env python3
"""
Advanced medicinal chemistry workflow.

Article:
Medicinal Chemistry and Drug Discovery

This script uses synthetic compound and assay data to calculate:

- pIC50 and potency classes
- selectivity windows
- ligand efficiency and lipophilic ligand efficiency
- Lipinski and Veber-style property checks
- hERG, CYP, solubility, permeability, and stability risk flags
- pharmacokinetic intuition proxies
- multiparameter optimization score
- project-level summaries
- Pareto frontier candidates
- Monte Carlo advancement probability
- potency/logP optimization scenarios
- assay progression decision matrix

This is educational scaffolding only. It is not a clinical decision system,
patient-treatment tool, dosing model, regulatory submission, toxicology
determination, synthesis protocol, controlled-substance design workflow,
biological-weapons workflow, or substitute for qualified professional review.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "medicinal_chemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "ic50_nM",
    "off_target_ic50_nM",
    "hERG_ic50_uM",
    "cyp3a4_ic50_uM",
    "solubility_uM",
    "permeability_10_6_cm_s",
    "microsomal_half_life_min",
    "plasma_protein_binding_percent",
    "clearance_mL_min_kg",
    "vd_L_kg",
    "molecular_weight",
    "clogP",
    "tpsa",
    "hbd",
    "hba",
    "rotatable_bonds",
    "fsp3",
    "aromatic_rings",
    "formal_charge",
    "synthetic_accessibility_score",
    "alert_count",
    "assay_qc_score",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp a value to a closed interval."""
    return max(low, min(high, value))


def parse_value(key: str, value: str):
    """Parse CSV values into numbers where appropriate."""
    if key in NUMERIC_FIELDS:
        return float(value)
    return value


def load_rows(path: Path = DATA_FILE) -> list[dict]:
    """Load synthetic medicinal chemistry records."""
    rows: list[dict] = []

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(key, value) for key, value in row.items()})

    return rows


def pIC50_from_nM(ic50_nM: float) -> float:
    """Convert IC50 in nM to pIC50."""
    if ic50_nM <= 0:
        return 0.0
    molar = ic50_nM * 1e-9
    return -math.log10(molar)


def potency_score(ic50_nM: float) -> float:
    """Bounded potency score where lower IC50 is better."""
    pic50 = pIC50_from_nM(ic50_nM)
    return clamp((pic50 - 5.0) / 3.0)


def selectivity_window(off_target_ic50_nM: float, on_target_ic50_nM: float) -> float:
    """Calculate off-target / on-target selectivity window."""
    if on_target_ic50_nM <= 0:
        return 0.0
    return off_target_ic50_nM / on_target_ic50_nM


def selectivity_score(window: float) -> float:
    """Bounded selectivity score."""
    return clamp(math.log10(max(window, 1.0)) / 3.0)


def ligand_efficiency(ic50_nM: float, heavy_atom_count_proxy: float) -> float:
    """
    Approximate ligand efficiency using pIC50 / heavy atom count proxy.

    Heavy atom count is approximated from molecular weight for this synthetic,
    dependency-free workflow.
    """
    heavy_atoms = max(heavy_atom_count_proxy, 1.0)
    return pIC50_from_nM(ic50_nM) / heavy_atoms


def heavy_atom_count_proxy(molecular_weight: float) -> float:
    """Approximate heavy atom count from molecular weight."""
    return molecular_weight / 14.0


def lipophilic_ligand_efficiency(ic50_nM: float, clogP: float) -> float:
    """Calculate lipophilic ligand efficiency proxy: LLE = pIC50 - cLogP."""
    return pIC50_from_nM(ic50_nM) - clogP


def lipinski_violations(row: dict) -> int:
    """Count simple Lipinski-style violations."""
    violations = 0
    violations += int(row["molecular_weight"] > 500)
    violations += int(row["clogP"] > 5)
    violations += int(row["hbd"] > 5)
    violations += int(row["hba"] > 10)
    return violations


def veber_violations(row: dict) -> int:
    """Count simple Veber-style violations."""
    violations = 0
    violations += int(row["tpsa"] > 140)
    violations += int(row["rotatable_bonds"] > 10)
    return violations


def solubility_score(solubility_uM: float) -> float:
    """Bounded solubility score."""
    return clamp(math.log10(max(solubility_uM, 0.001)) / 2.3)


def permeability_score(permeability_10_6_cm_s: float) -> float:
    """Bounded permeability score."""
    return clamp(permeability_10_6_cm_s / 30.0)


def microsomal_stability_score(microsomal_half_life_min: float) -> float:
    """Bounded metabolic stability score."""
    return clamp(microsomal_half_life_min / 90.0)


def hERG_risk_score(hERG_ic50_uM: float) -> float:
    """
    hERG risk proxy.

    Lower hERG IC50 suggests higher risk. This is a simplified screen,
    not a cardiac safety determination.
    """
    return clamp((10.0 - hERG_ic50_uM) / 10.0)


def cyp_inhibition_risk_score(cyp3a4_ic50_uM: float) -> float:
    """
    CYP3A4 inhibition risk proxy.

    Lower IC50 suggests higher inhibition risk. This is a simplified screen.
    """
    return clamp((20.0 - cyp3a4_ic50_uM) / 20.0)


def ppb_risk_score(plasma_protein_binding_percent: float) -> float:
    """Very high plasma protein binding risk proxy."""
    return clamp((plasma_protein_binding_percent - 95.0) / 5.0)


def clearance_score(clearance_mL_min_kg: float) -> float:
    """Bounded clearance score where lower clearance is better."""
    return clamp((45.0 - clearance_mL_min_kg) / 45.0)


def vd_reasonableness_score(vd_L_kg: float) -> float:
    """Bounded volume-of-distribution reasonableness score."""
    if vd_L_kg < 0.2:
        return 0.3
    if vd_L_kg <= 5.0:
        return 1.0
    return clamp((8.0 - vd_L_kg) / 3.0)


def oral_property_score(row: dict) -> float:
    """Composite property score for oral small-molecule-like behavior."""
    lipinski = lipinski_violations(row)
    veber = veber_violations(row)

    return clamp(
        0.22 * (1.0 - lipinski / 4.0)
        + 0.18 * (1.0 - veber / 2.0)
        + 0.18 * solubility_score(row["solubility_uM"])
        + 0.18 * permeability_score(row["permeability_10_6_cm_s"])
        + 0.14 * microsomal_stability_score(row["microsomal_half_life_min"])
        + 0.10 * clamp(row["fsp3"])
    )


def safety_liability_score(row: dict) -> float:
    """
    Safety-liability score where higher is worse.

    This is a discovery-screening proxy, not a toxicology conclusion.
    """
    return clamp(
        0.35 * hERG_risk_score(row["hERG_ic50_uM"])
        + 0.25 * cyp_inhibition_risk_score(row["cyp3a4_ic50_uM"])
        + 0.15 * ppb_risk_score(row["plasma_protein_binding_percent"])
        + 0.15 * clamp(row["alert_count"] / 3.0)
        + 0.10 * clamp((row["aromatic_rings"] - 3.0) / 3.0)
    )


def developability_score(row: dict) -> float:
    """Composite developability score."""
    return clamp(
        0.35 * oral_property_score(row)
        + 0.25 * clearance_score(row["clearance_mL_min_kg"])
        + 0.15 * vd_reasonableness_score(row["vd_L_kg"])
        + 0.15 * (1.0 - safety_liability_score(row))
        + 0.10 * (1.0 - clamp((row["synthetic_accessibility_score"] - 2.0) / 4.0))
    )


def multiparameter_optimization_score(row: dict) -> float:
    """
    Multiparameter optimization score.

    Balances potency, selectivity, LLE, oral property fit, developability,
    safety-liability avoidance, synthetic tractability, and assay quality.
    """
    pic50 = pIC50_from_nM(row["ic50_nM"])
    lle = lipophilic_ligand_efficiency(row["ic50_nM"], row["clogP"])
    window = selectivity_window(row["off_target_ic50_nM"], row["ic50_nM"])

    potency = potency_score(row["ic50_nM"])
    selectivity = selectivity_score(window)
    lle_score = clamp((lle - 2.0) / 5.0)
    property_fit = oral_property_score(row)
    developability = developability_score(row)
    safety = 1.0 - safety_liability_score(row)
    synthetic = 1.0 - clamp((row["synthetic_accessibility_score"] - 2.0) / 4.0)

    return clamp(
        0.20 * potency
        + 0.16 * selectivity
        + 0.14 * lle_score
        + 0.16 * property_fit
        + 0.16 * developability
        + 0.10 * safety
        + 0.04 * synthetic
        + 0.04 * row["assay_qc_score"]
    )


def advancement_recommendation(score: float, safety_liability: float, lipinski: int, alerts: float) -> str:
    """Translate score and risk into a discovery-stage recommendation."""
    if safety_liability >= 0.65 or alerts >= 2:
        return "deprioritize_or_redesign"
    if score >= 0.72 and lipinski <= 1:
        return "advance_to_integrated_profiling"
    if score >= 0.55:
        return "optimize_with_targeted_risk_reduction"
    return "hold_or_redesign"


def deterministic_seed(text: str) -> int:
    """Stable deterministic seed from a string."""
    total = 0
    for index, char in enumerate(text):
        total += (index + 1) * ord(char)
    return total % 100000


def monte_carlo_advancement_probability(row: dict, draws: int = 1000) -> dict:
    """
    Estimate probability of meeting an advancement score threshold using
    synthetic uncertainty around potency, selectivity, hERG, solubility, and QC.

    This is a teaching model, not a decision-grade uncertainty model.
    """
    rng = random.Random(deterministic_seed(row["compound_id"]))

    successes = 0
    scores = []

    for _ in range(draws):
        simulated = dict(row)
        simulated["ic50_nM"] = max(0.001, row["ic50_nM"] * rng.lognormvariate(0.0, 0.20))
        simulated["off_target_ic50_nM"] = max(0.001, row["off_target_ic50_nM"] * rng.lognormvariate(0.0, 0.25))
        simulated["hERG_ic50_uM"] = max(0.001, row["hERG_ic50_uM"] * rng.lognormvariate(0.0, 0.30))
        simulated["solubility_uM"] = max(0.001, row["solubility_uM"] * rng.lognormvariate(0.0, 0.25))
        simulated["permeability_10_6_cm_s"] = max(0.001, row["permeability_10_6_cm_s"] * rng.lognormvariate(0.0, 0.20))
        simulated["assay_qc_score"] = clamp(row["assay_qc_score"] + rng.gauss(0.0, 0.03))

        score = multiparameter_optimization_score(simulated)
        scores.append(score)

        if score >= 0.65 and safety_liability_score(simulated) < 0.55:
            successes += 1

    scores.sort()

    def percentile(p: float) -> float:
        index = int(round((p / 100.0) * (len(scores) - 1)))
        return scores[index]

    return {
        "mc_advancement_probability": successes / draws,
        "mc_score_p05": percentile(5),
        "mc_score_p50": percentile(50),
        "mc_score_p95": percentile(95),
        "mc_draws": draws,
    }


def enrich_row(row: dict) -> dict:
    """Add advanced medicinal chemistry indicators to one row."""
    pic50 = pIC50_from_nM(row["ic50_nM"])
    window = selectivity_window(row["off_target_ic50_nM"], row["ic50_nM"])
    hac = heavy_atom_count_proxy(row["molecular_weight"])
    le = ligand_efficiency(row["ic50_nM"], hac)
    lle = lipophilic_ligand_efficiency(row["ic50_nM"], row["clogP"])

    lipinski = lipinski_violations(row)
    veber = veber_violations(row)
    oral_score = oral_property_score(row)
    safety_score = safety_liability_score(row)
    developability = developability_score(row)
    mpo = multiparameter_optimization_score(row)
    mc = monte_carlo_advancement_probability(row)

    recommendation = advancement_recommendation(
        score=mpo,
        safety_liability=safety_score,
        lipinski=lipinski,
        alerts=row["alert_count"],
    )

    return {
        **row,
        "pIC50": pic50,
        "selectivity_window": window,
        "heavy_atom_count_proxy": hac,
        "ligand_efficiency_proxy": le,
        "lipophilic_ligand_efficiency": lle,
        "lipinski_violations": lipinski,
        "veber_violations": veber,
        "solubility_score": solubility_score(row["solubility_uM"]),
        "permeability_score": permeability_score(row["permeability_10_6_cm_s"]),
        "microsomal_stability_score": microsomal_stability_score(row["microsomal_half_life_min"]),
        "hERG_risk_score": hERG_risk_score(row["hERG_ic50_uM"]),
        "cyp3a4_risk_score": cyp_inhibition_risk_score(row["cyp3a4_ic50_uM"]),
        "ppb_risk_score": ppb_risk_score(row["plasma_protein_binding_percent"]),
        "clearance_score": clearance_score(row["clearance_mL_min_kg"]),
        "vd_reasonableness_score": vd_reasonableness_score(row["vd_L_kg"]),
        "oral_property_score": oral_score,
        "safety_liability_score": safety_score,
        "developability_score": developability,
        "multiparameter_optimization_score": mpo,
        **mc,
        "advancement_recommendation": recommendation,
    }


def is_dominated(candidate: dict, others: list[dict]) -> bool:
    """
    Determine whether a compound is dominated in a simplified Pareto sense.

    Objectives:
    - maximize MPO score
    - maximize selectivity window
    - maximize LLE
    - minimize safety liability
    """
    for other in others:
        if other["compound_id"] == candidate["compound_id"]:
            continue

        better_or_equal = (
            other["multiparameter_optimization_score"] >= candidate["multiparameter_optimization_score"]
            and other["selectivity_window"] >= candidate["selectivity_window"]
            and other["lipophilic_ligand_efficiency"] >= candidate["lipophilic_ligand_efficiency"]
            and other["safety_liability_score"] <= candidate["safety_liability_score"]
        )

        strictly_better = (
            other["multiparameter_optimization_score"] > candidate["multiparameter_optimization_score"]
            or other["selectivity_window"] > candidate["selectivity_window"]
            or other["lipophilic_ligand_efficiency"] > candidate["lipophilic_ligand_efficiency"]
            or other["safety_liability_score"] < candidate["safety_liability_score"]
        )

        if better_or_equal and strictly_better:
            return True

    return False


def pareto_frontier(indicators: list[dict]) -> list[dict]:
    """Return simplified Pareto frontier compounds."""
    frontier = []

    for row in indicators:
        if not is_dominated(row, indicators):
            frontier.append(
                {
                    "compound_id": row["compound_id"],
                    "project": row["project"],
                    "target": row["target"],
                    "pIC50": row["pIC50"],
                    "selectivity_window": row["selectivity_window"],
                    "lipophilic_ligand_efficiency": row["lipophilic_ligand_efficiency"],
                    "safety_liability_score": row["safety_liability_score"],
                    "multiparameter_optimization_score": row["multiparameter_optimization_score"],
                    "advancement_recommendation": row["advancement_recommendation"],
                }
            )

    return sorted(frontier, key=lambda item: item["multiparameter_optimization_score"], reverse=True)


def summarize_by_project(indicators: list[dict]) -> list[dict]:
    """Summarize indicators by discovery project."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["project"], []).append(row)

    summaries: list[dict] = []

    for project, records in sorted(grouped.items()):
        summaries.append(
            {
                "project": project,
                "n": len(records),
                "mean_pIC50": mean(row["pIC50"] for row in records),
                "best_pIC50": max(row["pIC50"] for row in records),
                "mean_selectivity_window": mean(row["selectivity_window"] for row in records),
                "mean_lipophilic_ligand_efficiency": mean(row["lipophilic_ligand_efficiency"] for row in records),
                "mean_oral_property_score": mean(row["oral_property_score"] for row in records),
                "mean_safety_liability_score": mean(row["safety_liability_score"] for row in records),
                "mean_developability_score": mean(row["developability_score"] for row in records),
                "mean_multiparameter_optimization_score": mean(row["multiparameter_optimization_score"] for row in records),
                "advance_count": sum(row["advancement_recommendation"] == "advance_to_integrated_profiling" for row in records),
            }
        )

    return summaries


def build_potency_lipophilicity_scenario(base_row: dict) -> list[dict]:
    """
    Build scenario grid for potency improvement and logP drift.

    Useful for visualizing potency-lipophilicity tradeoffs.
    """
    rows = []

    potency_multipliers = [0.10, 0.25, 0.50, 1.00, 2.00]
    logp_shifts = [-1.0, -0.5, 0.0, 0.5, 1.0]

    for potency_multiplier in potency_multipliers:
        for logp_shift in logp_shifts:
            modeled = dict(base_row)
            modeled["ic50_nM"] = max(0.001, base_row["ic50_nM"] * potency_multiplier)
            modeled["clogP"] = base_row["clogP"] + logp_shift

            rows.append(
                {
                    "scenario": "potency_lipophilicity_tradeoff",
                    "compound_id": base_row["compound_id"],
                    "potency_multiplier": potency_multiplier,
                    "clogP_shift": logp_shift,
                    "modeled_ic50_nM": modeled["ic50_nM"],
                    "modeled_clogP": modeled["clogP"],
                    "modeled_pIC50": pIC50_from_nM(modeled["ic50_nM"]),
                    "modeled_LLE": lipophilic_ligand_efficiency(modeled["ic50_nM"], modeled["clogP"]),
                    "modeled_MPO_score": multiparameter_optimization_score(modeled),
                }
            )

    return rows


def build_admet_rescue_scenario(base_row: dict) -> list[dict]:
    """
    Build ADMET rescue scenario grid.

    This explores improvements in solubility, hERG margin, and metabolic
    stability without proposing structural changes or synthesis routes.
    """
    rows = []

    solubility_multipliers = [1.0, 2.0, 5.0]
    hERG_multipliers = [1.0, 2.0, 4.0]
    stability_multipliers = [1.0, 1.5, 2.5]

    for sol_mult in solubility_multipliers:
        for herg_mult in hERG_multipliers:
            for stability_mult in stability_multipliers:
                modeled = dict(base_row)
                modeled["solubility_uM"] = base_row["solubility_uM"] * sol_mult
                modeled["hERG_ic50_uM"] = base_row["hERG_ic50_uM"] * herg_mult
                modeled["microsomal_half_life_min"] = base_row["microsomal_half_life_min"] * stability_mult

                rows.append(
                    {
                        "scenario": "admet_rescue",
                        "compound_id": base_row["compound_id"],
                        "solubility_multiplier": sol_mult,
                        "hERG_multiplier": herg_mult,
                        "stability_multiplier": stability_mult,
                        "modeled_solubility_uM": modeled["solubility_uM"],
                        "modeled_hERG_ic50_uM": modeled["hERG_ic50_uM"],
                        "modeled_microsomal_half_life_min": modeled["microsomal_half_life_min"],
                        "modeled_safety_liability_score": safety_liability_score(modeled),
                        "modeled_developability_score": developability_score(modeled),
                        "modeled_MPO_score": multiparameter_optimization_score(modeled),
                    }
                )

    return rows


def build_assay_progression_matrix() -> list[dict]:
    """Build professional discovery-stage assay progression matrix."""
    return [
        {
            "stage": "primary_biochemical_screen",
            "objective": "confirm target engagement signal",
            "decision_evidence": "potency, curve quality, assay interference review",
            "advance_condition": "reproducible concentration-response with acceptable QC",
        },
        {
            "stage": "orthogonal_assay",
            "objective": "reduce assay-artifact risk",
            "decision_evidence": "orthogonal potency, counterscreen, mechanism consistency",
            "advance_condition": "activity transfers to independent assay format",
        },
        {
            "stage": "cellular_activity",
            "objective": "test cellular translation",
            "decision_evidence": "cell potency, permeability, cytotoxicity separation",
            "advance_condition": "cell activity with reasonable exposure and selectivity",
        },
        {
            "stage": "early_admet_panel",
            "objective": "identify developability liabilities",
            "decision_evidence": "solubility, permeability, microsomal stability, CYP, hERG",
            "advance_condition": "manageable liabilities or clear optimization path",
        },
        {
            "stage": "selectivity_panel",
            "objective": "evaluate target-family and safety pharmacology risks",
            "decision_evidence": "off-target windows, family panel profile, pharmacology flags",
            "advance_condition": "adequate selectivity margin for project stage",
        },
        {
            "stage": "integrated_lead_optimization",
            "objective": "balance potency, selectivity, ADMET, and tractability",
            "decision_evidence": "MPO score, project hypothesis, structure-property trends",
            "advance_condition": "improving profile across multiple independent dimensions",
        },
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write rows to CSV using union fieldnames."""
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(indicators: list[dict], summaries: list[dict], frontier: list[dict]) -> None:
    """Write an advanced Markdown report."""
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    advance = [
        row for row in indicators
        if row["advancement_recommendation"] == "advance_to_integrated_profiling"
    ]

    redesign = [
        row for row in indicators
        if row["advancement_recommendation"] == "deprioritize_or_redesign"
    ]

    lines = [
        "# Advanced Medicinal Chemistry Report",
        "",
        "This report summarizes synthetic medicinal chemistry decision indicators for the article **Medicinal Chemistry and Drug Discovery**.",
        "",
        f"Total compounds: {len(indicators)}",
        f"Recommended for integrated profiling: {len(advance)}",
        f"Recommended for deprioritization/redesign: {len(redesign)}",
        f"Pareto frontier compounds: {len(frontier)}",
        "",
        "## Pareto frontier compounds",
        "",
    ]

    for row in frontier:
        lines.append(
            f"- {row['compound_id']} ({row['project']}): "
            f"pIC50={row['pIC50']:.2f}, "
            f"selectivity window={row['selectivity_window']:.1f}, "
            f"LLE={row['lipophilic_ligand_efficiency']:.2f}, "
            f"safety liability={row['safety_liability_score']:.3f}, "
            f"MPO={row['multiparameter_optimization_score']:.3f}, "
            f"recommendation={row['advancement_recommendation']}"
        )

    lines.extend(["", "## Project summaries", ""])

    for row in summaries:
        lines.append(
            f"- {row['project']}: "
            f"n={row['n']}, "
            f"best pIC50={row['best_pIC50']:.2f}, "
            f"mean selectivity={row['mean_selectivity_window']:.1f}, "
            f"mean LLE={row['mean_lipophilic_ligand_efficiency']:.2f}, "
            f"mean developability={row['mean_developability_score']:.3f}, "
            f"mean MPO={row['mean_multiparameter_optimization_score']:.3f}, "
            f"advance count={row['advance_count']}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not clinical recommendations, patient-treatment guidance, dosing advice, regulatory conclusions, toxicology findings, synthesis protocols, controlled-substance design instructions, or substitutes for qualified medicinal chemistry, pharmacology, toxicology, clinical, legal, or regulatory review.",
        ]
    )

    (OUT_REPORTS / "advanced_medicinal_chemistry_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(
    indicators: list[dict],
    summaries: list[dict],
    frontier: list[dict],
    potency_scenarios: list[dict],
    admet_scenarios: list[dict],
    assay_matrix: list[dict],
) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "medicinal-chemistry-drug-discovery",
        "title": "Medicinal Chemistry and Drug Discovery",
        "advanced_layer": True,
        "synthetic_compounds": len(indicators),
        "project_summary_rows": len(summaries),
        "pareto_frontier_rows": len(frontier),
        "potency_lipophilicity_scenario_rows": len(potency_scenarios),
        "admet_rescue_scenario_rows": len(admet_scenarios),
        "assay_matrix_rows": len(assay_matrix),
        "outputs": [
            "advanced/outputs/tables/advanced_medicinal_chemistry_indicators.csv",
            "advanced/outputs/tables/advanced_project_summary.csv",
            "advanced/outputs/tables/advanced_pareto_frontier.csv",
            "advanced/outputs/tables/advanced_potency_lipophilicity_scenarios.csv",
            "advanced/outputs/tables/advanced_admet_rescue_scenarios.csv",
            "advanced/outputs/tables/advanced_assay_progression_matrix.csv",
            "advanced/outputs/reports/advanced_medicinal_chemistry_report.md",
        ],
        "responsible_use": "Synthetic educational medicinal chemistry workflow only; not for clinical, regulatory, toxicology, dosing, synthesis, controlled-substance design, or patient-care decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced medicinal chemistry workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_project(indicators)
    frontier = pareto_frontier(indicators)

    best_candidate = max(indicators, key=lambda row: row["multiparameter_optimization_score"])
    risky_candidate = max(indicators, key=lambda row: row["safety_liability_score"])

    potency_scenarios = build_potency_lipophilicity_scenario(best_candidate)
    admet_scenarios = build_admet_rescue_scenario(risky_candidate)
    assay_matrix = build_assay_progression_matrix()

    write_csv(OUT_TABLES / "advanced_medicinal_chemistry_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_project_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_pareto_frontier.csv", frontier)
    write_csv(OUT_TABLES / "advanced_potency_lipophilicity_scenarios.csv", potency_scenarios)
    write_csv(OUT_TABLES / "advanced_admet_rescue_scenarios.csv", admet_scenarios)
    write_csv(OUT_TABLES / "advanced_assay_progression_matrix.csv", assay_matrix)

    write_report(indicators, summaries, frontier)
    write_manifest(indicators, summaries, frontier, potency_scenarios, admet_scenarios, assay_matrix)

    print("Advanced medicinal chemistry workflow complete.")
    print(f"Compounds: {len(indicators)}")
    print(f"Project summaries: {len(summaries)}")
    print(f"Pareto frontier compounds: {len(frontier)}")
    print(f"Potency/logP scenario rows: {len(potency_scenarios)}")
    print(f"ADMET rescue scenario rows: {len(admet_scenarios)}")
    print(f"Assay matrix rows: {len(assay_matrix)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
