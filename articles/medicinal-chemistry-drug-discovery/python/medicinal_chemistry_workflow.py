#!/usr/bin/env python3
"""
Medicinal chemistry decision analytics.

Synthetic educational workflow for:
- pIC50
- selectivity windows
- ligand efficiency proxy
- lipophilic ligand efficiency
- Lipinski and Veber-style filters
- ADMET risk flags
- multiparameter optimization
- Pareto frontier screening

No synthesis instructions, no clinical recommendations, no real compound claims.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean

ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "medicinal_chemistry_synthetic.csv"
OUT_TABLES = ARTICLE_DIR / "outputs" / "tables"
OUT_REPORTS = ARTICLE_DIR / "outputs" / "reports"
OUT_MANIFESTS = ARTICLE_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "ic50_nM", "off_target_ic50_nM", "hERG_ic50_uM", "cyp3a4_ic50_uM",
    "solubility_uM", "permeability_10_6_cm_s", "microsomal_half_life_min",
    "plasma_protein_binding_percent", "clearance_mL_min_kg", "vd_L_kg",
    "molecular_weight", "clogP", "tpsa", "hbd", "hba", "rotatable_bonds",
    "fsp3", "aromatic_rings", "formal_charge", "synthetic_accessibility_score",
    "alert_count", "assay_qc_score"
}

def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))

def parse_value(key, value):
    return float(value) if key in NUMERIC_FIELDS else value

def load_rows(path=DATA_FILE):
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [
            {key: parse_value(key, value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]

def pic50_from_nm(ic50_nm):
    return -math.log10(ic50_nm * 1e-9)

def selectivity_window(off_target_ic50_nm, target_ic50_nm):
    return off_target_ic50_nm / target_ic50_nm if target_ic50_nm > 0 else 0.0

def ligand_efficiency_proxy(ic50_nm, molecular_weight):
    heavy_atom_proxy = max(molecular_weight / 14.0, 1.0)
    return pic50_from_nm(ic50_nm) / heavy_atom_proxy

def lipophilic_ligand_efficiency(ic50_nm, clogp):
    return pic50_from_nm(ic50_nm) - clogp

def lipinski_violations(row):
    return int(row["molecular_weight"] > 500) + int(row["clogP"] > 5) + int(row["hbd"] > 5) + int(row["hba"] > 10)

def veber_violations(row):
    return int(row["tpsa"] > 140) + int(row["rotatable_bonds"] > 10)

def hERG_risk(row):
    return clamp((10.0 - row["hERG_ic50_uM"]) / 10.0)

def cyp3a4_risk(row):
    return clamp((20.0 - row["cyp3a4_ic50_uM"]) / 20.0)

def solubility_score(row):
    return clamp(math.log10(max(row["solubility_uM"], 0.001)) / 2.3)

def permeability_score(row):
    return clamp(row["permeability_10_6_cm_s"] / 30.0)

def stability_score(row):
    return clamp(row["microsomal_half_life_min"] / 90.0)

def safety_liability_score(row):
    return clamp(
        0.35 * hERG_risk(row)
        + 0.25 * cyp3a4_risk(row)
        + 0.15 * clamp((row["plasma_protein_binding_percent"] - 95.0) / 5.0)
        + 0.15 * clamp(row["alert_count"] / 3.0)
        + 0.10 * clamp((row["aromatic_rings"] - 3.0) / 3.0)
    )

def oral_property_score(row):
    return clamp(
        0.22 * (1.0 - lipinski_violations(row) / 4.0)
        + 0.18 * (1.0 - veber_violations(row) / 2.0)
        + 0.18 * solubility_score(row)
        + 0.18 * permeability_score(row)
        + 0.14 * stability_score(row)
        + 0.10 * clamp(row["fsp3"])
    )

def developability_score(row):
    clearance_score = clamp((45.0 - row["clearance_mL_min_kg"]) / 45.0)
    vd_score = 1.0 if 0.2 <= row["vd_L_kg"] <= 5.0 else 0.4
    synthetic_score = 1.0 - clamp((row["synthetic_accessibility_score"] - 2.0) / 4.0)
    return clamp(
        0.35 * oral_property_score(row)
        + 0.25 * clearance_score
        + 0.15 * vd_score
        + 0.15 * (1.0 - safety_liability_score(row))
        + 0.10 * synthetic_score
    )

def mpo_score(row):
    pic50 = pic50_from_nm(row["ic50_nM"])
    selectivity = selectivity_window(row["off_target_ic50_nM"], row["ic50_nM"])
    lle = lipophilic_ligand_efficiency(row["ic50_nM"], row["clogP"])
    return clamp(
        0.22 * clamp((pic50 - 5.0) / 3.0)
        + 0.17 * clamp(math.log10(max(selectivity, 1.0)) / 3.0)
        + 0.16 * clamp((lle - 2.0) / 5.0)
        + 0.17 * oral_property_score(row)
        + 0.16 * developability_score(row)
        + 0.08 * (1.0 - safety_liability_score(row))
        + 0.04 * row["assay_qc_score"]
    )

def recommendation(row):
    score = row["multiparameter_optimization_score"]
    safety = row["safety_liability_score"]
    if safety >= 0.65 or row["alert_count"] >= 2:
        return "deprioritize_or_redesign"
    if score >= 0.72 and row["lipinski_violations"] <= 1:
        return "advance_to_integrated_profiling"
    if score >= 0.55:
        return "optimize_with_targeted_risk_reduction"
    return "hold_or_redesign"

def enrich(row):
    enriched = {
        **row,
        "pIC50": pic50_from_nm(row["ic50_nM"]),
        "selectivity_window": selectivity_window(row["off_target_ic50_nM"], row["ic50_nM"]),
        "ligand_efficiency_proxy": ligand_efficiency_proxy(row["ic50_nM"], row["molecular_weight"]),
        "lipophilic_ligand_efficiency": lipophilic_ligand_efficiency(row["ic50_nM"], row["clogP"]),
        "lipinski_violations": lipinski_violations(row),
        "veber_violations": veber_violations(row),
        "oral_property_score": oral_property_score(row),
        "safety_liability_score": safety_liability_score(row),
        "developability_score": developability_score(row),
    }
    enriched["multiparameter_optimization_score"] = mpo_score(enriched)
    enriched["advancement_recommendation"] = recommendation(enriched)
    return enriched

def pareto_frontier(rows):
    frontier = []
    for row in rows:
        dominated = False
        for other in rows:
            if other["compound_id"] == row["compound_id"]:
                continue
            better_or_equal = (
                other["multiparameter_optimization_score"] >= row["multiparameter_optimization_score"]
                and other["selectivity_window"] >= row["selectivity_window"]
                and other["lipophilic_ligand_efficiency"] >= row["lipophilic_ligand_efficiency"]
                and other["safety_liability_score"] <= row["safety_liability_score"]
            )
            strictly_better = (
                other["multiparameter_optimization_score"] > row["multiparameter_optimization_score"]
                or other["selectivity_window"] > row["selectivity_window"]
                or other["lipophilic_ligand_efficiency"] > row["lipophilic_ligand_efficiency"]
                or other["safety_liability_score"] < row["safety_liability_score"]
            )
            if better_or_equal and strictly_better:
                dominated = True
                break
        if not dominated:
            frontier.append(row)
    return frontier

def summarize_by_project(rows):
    grouped = {}
    for row in rows:
        grouped.setdefault(row["project"], []).append(row)
    summary = []
    for project, records in sorted(grouped.items()):
        summary.append({
            "project": project,
            "n": len(records),
            "mean_pIC50": mean(r["pIC50"] for r in records),
            "best_pIC50": max(r["pIC50"] for r in records),
            "mean_LLE": mean(r["lipophilic_ligand_efficiency"] for r in records),
            "mean_MPO": mean(r["multiparameter_optimization_score"] for r in records),
            "advance_count": sum(r["advancement_recommendation"] == "advance_to_integrated_profiling" for r in records),
        })
    return summary

def write_csv(path, rows):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    rows = [enrich(row) for row in load_rows()]
    frontier = pareto_frontier(rows)
    summary = summarize_by_project(rows)

    write_csv(OUT_TABLES / "medicinal_chemistry_indicators.csv", rows)
    write_csv(OUT_TABLES / "project_summary.csv", summary)
    write_csv(OUT_TABLES / "pareto_frontier.csv", frontier)

    report = [
        "# Medicinal Chemistry Decision Analytics Report",
        "",
        f"Compounds: {len(rows)}",
        f"Pareto frontier compounds: {len(frontier)}",
        f"Advance recommendations: {sum(r['advancement_recommendation'] == 'advance_to_integrated_profiling' for r in rows)}",
        "",
        "Synthetic educational data only. No clinical, synthesis, toxicology, or regulatory conclusions."
    ]
    (OUT_REPORTS / "medicinal_chemistry_report.md").write_text("\n".join(report), encoding="utf-8")

    manifest = {
        "article_slug": "medicinal-chemistry-drug-discovery",
        "outputs": [
            "outputs/tables/medicinal_chemistry_indicators.csv",
            "outputs/tables/project_summary.csv",
            "outputs/tables/pareto_frontier.csv",
            "outputs/reports/medicinal_chemistry_report.md"
        ],
        "responsible_use": "Synthetic educational medicinal chemistry decision analytics only."
    }
    (OUT_MANIFESTS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Medicinal chemistry workflow complete.")

if __name__ == "__main__":
    main()
