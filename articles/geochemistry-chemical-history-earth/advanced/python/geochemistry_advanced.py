#!/usr/bin/env python3
"""
Advanced geochemistry workflow.

Article:
Geochemistry and the Chemical History of Earth

This script uses synthetic geochemical data to calculate:

- major-oxide molar proportions
- Chemical Index of Alteration, weight-based and molar
- CaO* correction proxy for silicate calcium
- trace-element ratios
- isotope delta notation
- simplified parent-daughter radiometric ages
- rare-earth-element normalization
- redox archive and weathering pressure indicators
- two-component isotope mixing series
- radiogenic decay series
- grouped summaries by rock type

This is educational scaffolding only. It is not a professional geochemical
interpretation, geochronology report, exploration tool, resource estimate,
contamination assessment, or legal/regulatory analysis.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "geochemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "SiO2_wt_pct",
    "Al2O3_wt_pct",
    "FeO_total_wt_pct",
    "MgO_wt_pct",
    "CaO_wt_pct",
    "Na2O_wt_pct",
    "K2O_wt_pct",
    "TiO2_wt_pct",
    "P2O5_wt_pct",
    "Rb_ppm",
    "Sr_ppm",
    "Zr_ppm",
    "Y_ppm",
    "La_ppm",
    "Ce_ppm",
    "Nd_ppm",
    "Sm_ppm",
    "Yb_ppm",
    "U_ppm",
    "Th_ppm",
    "parent_isotope_units",
    "radiogenic_daughter_units",
    "sample_ratio",
    "standard_ratio",
    "delta13C_permil",
    "delta18O_permil",
    "qc_score",
}

OXIDE_MOLAR_MASS = {
    "SiO2": 60.0843,
    "Al2O3": 101.9613,
    "FeO": 71.844,
    "MgO": 40.3044,
    "CaO": 56.0774,
    "Na2O": 61.9789,
    "K2O": 94.196,
    "TiO2": 79.866,
    "P2O5": 141.9445,
}

# Small synthetic normalizing reservoir for demonstration only.
# These are not a substitute for a chosen chondrite, primitive mantle, or shale standard.
REE_REFERENCE_PPM = {
    "La": 0.237,
    "Ce": 0.613,
    "Nd": 0.457,
    "Sm": 0.153,
    "Yb": 0.165,
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
    """Load synthetic geochemical records."""
    rows: list[dict] = []

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(key, value) for key, value in row.items()})

    return rows


def oxide_moles(wt_pct: float, oxide_key: str) -> float:
    """Convert oxide weight percent to molar proportion proxy."""
    return wt_pct / OXIDE_MOLAR_MASS[oxide_key]


def cao_star_moles(row: dict) -> float:
    """
    Estimate CaO* for CIA-like weathering calculations.

    This is a simplified educational correction. A common teaching correction
    subtracts a phosphate-associated calcium term and limits the result so that
    corrected silicate CaO does not exceed Na2O on a molar basis in weathered
    sedimentary materials.

    Research workflows must inspect carbonates, phosphates, mineralogy,
    petrography, and parent material.
    """
    cao = oxide_moles(row["CaO_wt_pct"], "CaO")
    p2o5 = oxide_moles(row["P2O5_wt_pct"], "P2O5")
    na2o = oxide_moles(row["Na2O_wt_pct"], "Na2O")

    # Apatite correction proxy: CaO associated with P2O5.
    corrected = max(cao - (10.0 / 3.0) * p2o5, 0.0)

    if row["material"] in {"sedimentary_rock", "regolith"}:
        corrected = min(corrected, na2o)

    return corrected


def cia_weight_based(row: dict) -> float:
    """
    Simplified CIA using oxide weight percentages.

    This is useful pedagogically but less rigorous than a molar calculation.
    """
    denominator = (
        row["Al2O3_wt_pct"]
        + row["CaO_wt_pct"]
        + row["Na2O_wt_pct"]
        + row["K2O_wt_pct"]
    )

    return 100.0 * row["Al2O3_wt_pct"] / denominator


def cia_molar(row: dict) -> float:
    """
    Molar Chemical Index of Alteration with simplified CaO* correction.

    CIA = 100 * Al2O3 / (Al2O3 + CaO* + Na2O + K2O)
    """
    al = oxide_moles(row["Al2O3_wt_pct"], "Al2O3")
    ca_star = cao_star_moles(row)
    na = oxide_moles(row["Na2O_wt_pct"], "Na2O")
    k = oxide_moles(row["K2O_wt_pct"], "K2O")

    denominator = al + ca_star + na + k
    return 100.0 * al / denominator if denominator > 0 else 0.0


def ratio_safe(numerator: float, denominator: float) -> float:
    """Safe ratio calculation."""
    if denominator == 0:
        return 0.0
    return numerator / denominator


def isotope_delta(sample_ratio: float, standard_ratio: float) -> float:
    """
    Delta notation.

    delta = ((R_sample / R_standard) - 1) * 1000
    """
    return ((sample_ratio / standard_ratio) - 1.0) * 1000.0


def radiometric_age_ma(
    parent: float,
    daughter: float,
    decay_constant_per_year: float = 1.55125e-10,
) -> float:
    """
    Simplified parent-daughter radiometric age.

    t = (1/lambda) * ln(1 + D/P)

    Assumes no initial daughter and closed-system behavior.
    """
    if parent <= 0:
        return 0.0

    age_years = (1.0 / decay_constant_per_year) * math.log(1.0 + daughter / parent)
    return age_years / 1.0e6


def ree_normalized(row: dict) -> dict:
    """Calculate simplified REE-normalized values."""
    return {
        "La_N": row["La_ppm"] / REE_REFERENCE_PPM["La"],
        "Ce_N": row["Ce_ppm"] / REE_REFERENCE_PPM["Ce"],
        "Nd_N": row["Nd_ppm"] / REE_REFERENCE_PPM["Nd"],
        "Sm_N": row["Sm_ppm"] / REE_REFERENCE_PPM["Sm"],
        "Yb_N": row["Yb_ppm"] / REE_REFERENCE_PPM["Yb"],
    }


def europium_anomaly_proxy(normalized: dict) -> float:
    """
    Approximate Eu anomaly proxy without Eu.

    Since the synthetic dataset does not include Eu, this uses Sm and Nd/Yb
    curvature as a placeholder diagnostic. It is not a real Eu anomaly.
    """
    denominator = math.sqrt(normalized["Nd_N"] * normalized["Yb_N"])
    if denominator <= 0:
        return 0.0
    return normalized["Sm_N"] / denominator


def light_to_heavy_ree_ratio(normalized: dict) -> float:
    """Calculate La_N/Yb_N as a light-to-heavy REE enrichment proxy."""
    return ratio_safe(normalized["La_N"], normalized["Yb_N"])


def redox_archive_index(row: dict) -> float:
    """
    Build a simplified redox archive index.

    Stronger values come from iron-rich samples, chemical sediments,
    shales/sulfides, and isotope shifts.
    """
    fe_si = ratio_safe(row["FeO_total_wt_pct"], row["SiO2_wt_pct"])
    isotope_shift = clamp(abs(row["delta13C_permil"]) / 25.0)
    material_bonus = 0.25 if row["rock_type"] in {"banded_iron_formation", "shale", "sulfide"} else 0.0
    oxygen_shift = clamp(abs(row["delta18O_permil"]) / 18.0)

    return clamp(0.35 * clamp(fe_si / 0.8) + 0.25 * isotope_shift + 0.20 * oxygen_shift + material_bonus)


def geochemical_archive_index(row: dict, cia: float, lree_hree: float, redox_index: float) -> float:
    """
    Composite teaching index for chemically informative archive strength.

    This is not a scientific score. It organizes several indicators for
    article-supporting computation.
    """
    weathering_component = clamp(cia / 100.0)
    trace_component = clamp(ratio_safe(row["Rb_ppm"], row["Sr_ppm"]))
    ree_component = clamp(math.log1p(lree_hree) / math.log(10))
    redox_component = redox_index
    qc_component = row["qc_score"]

    return clamp(
        0.25 * weathering_component
        + 0.20 * trace_component
        + 0.20 * ree_component
        + 0.25 * redox_component
        + 0.10 * qc_component
    )


def enrich_row(row: dict) -> dict:
    """Add advanced geochemical indicators to one row."""
    normalized = ree_normalized(row)
    lree_hree = light_to_heavy_ree_ratio(normalized)
    redox_index = redox_archive_index(row)
    cia_wt = cia_weight_based(row)
    cia_m = cia_molar(row)
    age_ma = radiometric_age_ma(
        row["parent_isotope_units"],
        row["radiogenic_daughter_units"],
    )

    archive_index = geochemical_archive_index(row, cia_m, lree_hree, redox_index)

    return {
        **row,
        "CIA_weight_based": cia_wt,
        "CIA_molar_CaO_star": cia_m,
        "CaO_star_moles_proxy": cao_star_moles(row),
        "Rb_Sr_ratio": ratio_safe(row["Rb_ppm"], row["Sr_ppm"]),
        "Th_U_ratio": ratio_safe(row["Th_ppm"], row["U_ppm"]),
        "Zr_Y_ratio": ratio_safe(row["Zr_ppm"], row["Y_ppm"]),
        "Fe_Si_ratio": ratio_safe(row["FeO_total_wt_pct"], row["SiO2_wt_pct"]),
        "delta_from_ratio_permil": isotope_delta(row["sample_ratio"], row["standard_ratio"]),
        "radiometric_age_Ma_simplified": age_ma,
        **normalized,
        "LaN_YbN_ratio": lree_hree,
        "Eu_anomaly_proxy_without_Eu": europium_anomaly_proxy(normalized),
        "redox_archive_index": redox_index,
        "geochemical_archive_index": archive_index,
        "attention_flag": "strong_archive_signal" if archive_index >= 0.55 else "general_archive_signal",
    }


def summarize_by_rock_type(indicators: list[dict]) -> list[dict]:
    """Summarize indicators by rock type."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["rock_type"], []).append(row)

    summaries: list[dict] = []

    for rock_type, records in sorted(grouped.items()):
        summaries.append(
            {
                "rock_type": rock_type,
                "n": len(records),
                "mean_SiO2_wt_pct": mean(row["SiO2_wt_pct"] for row in records),
                "mean_CIA_molar_CaO_star": mean(row["CIA_molar_CaO_star"] for row in records),
                "mean_Rb_Sr_ratio": mean(row["Rb_Sr_ratio"] for row in records),
                "mean_Th_U_ratio": mean(row["Th_U_ratio"] for row in records),
                "mean_LaN_YbN_ratio": mean(row["LaN_YbN_ratio"] for row in records),
                "mean_redox_archive_index": mean(row["redox_archive_index"] for row in records),
                "mean_geochemical_archive_index": mean(row["geochemical_archive_index"] for row in records),
            }
        )

    return summaries


def build_radiogenic_decay_series(
    parent_initial: float = 1.0,
    decay_constant_per_year: float = 1.55125e-10,
    max_age_ma: int = 3000,
    step_ma: int = 100,
) -> list[dict]:
    """Build a simplified radiogenic parent-daughter decay series."""
    rows: list[dict] = []

    for age_ma in range(0, max_age_ma + step_ma, step_ma):
        time_years = age_ma * 1.0e6
        parent_remaining = parent_initial * math.exp(-decay_constant_per_year * time_years)
        daughter_produced = parent_initial - parent_remaining

        rows.append(
            {
                "age_Ma": age_ma,
                "parent_remaining_units": parent_remaining,
                "radiogenic_daughter_units": daughter_produced,
                "daughter_parent_ratio": ratio_safe(daughter_produced, parent_remaining),
            }
        )

    return rows


def build_isotope_mixing_series(
    endmember_a: float = -25.0,
    endmember_b: float = 2.0,
    step_percent: int = 5,
) -> list[dict]:
    """Build a two-component isotope mixing series."""
    rows: list[dict] = []

    for percent_a in range(0, 101, step_percent):
        fraction_a = percent_a / 100.0
        fraction_b = 1.0 - fraction_a
        mixed_delta = fraction_a * endmember_a + fraction_b * endmember_b

        rows.append(
            {
                "fraction_endmember_A": fraction_a,
                "fraction_endmember_B": fraction_b,
                "delta_mixed_permil": mixed_delta,
                "endmember_A_delta_permil": endmember_a,
                "endmember_B_delta_permil": endmember_b,
            }
        )

    return rows


def build_weathering_trajectory_series(base_row: dict) -> list[dict]:
    """
    Build a synthetic weathering trajectory.

    The trajectory progressively removes CaO, Na2O, and K2O while enriching
    residual Al2O3, mimicking simplified chemical weathering.
    """
    rows: list[dict] = []

    for step in range(0, 21):
        intensity = step / 20.0

        modeled = dict(base_row)
        modeled["CaO_wt_pct"] = base_row["CaO_wt_pct"] * (1.0 - 0.85 * intensity)
        modeled["Na2O_wt_pct"] = base_row["Na2O_wt_pct"] * (1.0 - 0.75 * intensity)
        modeled["K2O_wt_pct"] = base_row["K2O_wt_pct"] * (1.0 - 0.35 * intensity)
        modeled["Al2O3_wt_pct"] = base_row["Al2O3_wt_pct"] * (1.0 + 0.35 * intensity)

        rows.append(
            {
                "weathering_step": step,
                "weathering_intensity": intensity,
                "modeled_CaO_wt_pct": modeled["CaO_wt_pct"],
                "modeled_Na2O_wt_pct": modeled["Na2O_wt_pct"],
                "modeled_K2O_wt_pct": modeled["K2O_wt_pct"],
                "modeled_Al2O3_wt_pct": modeled["Al2O3_wt_pct"],
                "modeled_CIA_molar_CaO_star": cia_molar(modeled),
            }
        )

    return rows


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


def write_report(indicators: list[dict], summaries: list[dict]) -> None:
    """Write an advanced Markdown report."""
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    strong_archives = [
        row for row in indicators
        if row["attention_flag"] == "strong_archive_signal"
    ]

    high_weathering = [
        row for row in indicators
        if row["CIA_molar_CaO_star"] >= 80
    ]

    redox_archives = [
        row for row in indicators
        if row["redox_archive_index"] >= 0.45
    ]

    lines = [
        "# Advanced Geochemistry Report",
        "",
        "This report summarizes synthetic geochemical indicators for the article **Geochemistry and the Chemical History of Earth**.",
        "",
        f"Total records: {len(indicators)}",
        f"Strong archive signals: {len(strong_archives)}",
        f"High weathering screens: {len(high_weathering)}",
        f"Redox archive screens: {len(redox_archives)}",
        "",
        "## Strong archive signals",
        "",
    ]

    for row in strong_archives:
        lines.append(
            f"- {row['sample_id']} ({row['rock_type']}): "
            f"CIA={row['CIA_molar_CaO_star']:.2f}, "
            f"Rb/Sr={row['Rb_Sr_ratio']:.3f}, "
            f"redox index={row['redox_archive_index']:.3f}, "
            f"archive index={row['geochemical_archive_index']:.3f}"
        )

    lines.extend(["", "## Rock-type summaries", ""])

    for row in summaries:
        lines.append(
            f"- {row['rock_type']}: "
            f"mean CIA={row['mean_CIA_molar_CaO_star']:.2f}, "
            f"mean LaN/YbN={row['mean_LaN_YbN_ratio']:.2f}, "
            f"mean archive index={row['mean_geochemical_archive_index']:.3f}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not professional geochemical interpretations, geochronology findings, mining assessments, contamination assessments, legal evidence, resource estimates, or regulatory determinations.",
        ]
    )

    (OUT_REPORTS / "advanced_geochemistry_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(
    indicators: list[dict],
    summaries: list[dict],
    decay_series: list[dict],
    mixing_series: list[dict],
    weathering_series: list[dict],
) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "geochemistry-chemical-history-earth",
        "title": "Geochemistry and the Chemical History of Earth",
        "advanced_layer": True,
        "synthetic_records": len(indicators),
        "summary_groups": len(summaries),
        "decay_series_rows": len(decay_series),
        "mixing_series_rows": len(mixing_series),
        "weathering_series_rows": len(weathering_series),
        "outputs": [
            "advanced/outputs/tables/advanced_geochemical_indicators.csv",
            "advanced/outputs/tables/advanced_rock_type_summary.csv",
            "advanced/outputs/tables/advanced_radiogenic_decay_series.csv",
            "advanced/outputs/tables/advanced_isotope_mixing_series.csv",
            "advanced/outputs/tables/advanced_weathering_trajectory.csv",
            "advanced/outputs/reports/advanced_geochemistry_report.md",
        ],
        "responsible_use": "Synthetic educational geochemistry workflow only; not for professional geochronology, mining, contamination, legal, resource, or regulatory decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced geochemistry workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_rock_type(indicators)
    decay_series = build_radiogenic_decay_series()
    mixing_series = build_isotope_mixing_series()
    weathering_series = build_weathering_trajectory_series(rows[0])

    write_csv(OUT_TABLES / "advanced_geochemical_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_rock_type_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_radiogenic_decay_series.csv", decay_series)
    write_csv(OUT_TABLES / "advanced_isotope_mixing_series.csv", mixing_series)
    write_csv(OUT_TABLES / "advanced_weathering_trajectory.csv", weathering_series)

    write_report(indicators, summaries)
    write_manifest(indicators, summaries, decay_series, mixing_series, weathering_series)

    print("Advanced geochemistry workflow complete.")
    print(f"Records: {len(indicators)}")
    print(f"Rock-type summaries: {len(summaries)}")
    print(f"Decay series rows: {len(decay_series)}")
    print(f"Mixing series rows: {len(mixing_series)}")
    print(f"Weathering trajectory rows: {len(weathering_series)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
