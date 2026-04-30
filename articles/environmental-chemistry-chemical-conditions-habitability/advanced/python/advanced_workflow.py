
#!/usr/bin/env python3
"""
Advanced computational layer for:
Environmental Chemistry and the Chemical Conditions of Habitability

This module is synthetic and educational. It provides reusable calculations,
model outputs, tests, reports, and provenance scaffolding. It is not a
professional regulatory, legal, operational, clinical, resource, or research-
grade decision tool.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean

CONFIG = {'title': 'Environmental Chemistry and the Chemical Conditions of Habitability', 'model_type': 'environmental', 'group_key': 'compartment', 'description': 'Advanced environmental chemistry workflows for chemical habitability, contaminant fate, exposure screening, decay, partitioning, and source-pathway-receptor evidence.', 'rows': [{'sample_id': 'ENV001', 'compartment': 'surface_water', 'analyte': 'nitrate', 'concentration': 8.2, 'benchmark': 10.0, 'unit': 'mg/L', 'half_life_days': 18, 'koc_L_kg': 5, 'organic_carbon_fraction': 0.02, 'exposure_weight': 0.55, 'monitoring_confidence': 0.92}, {'sample_id': 'ENV002', 'compartment': 'groundwater', 'analyte': 'arsenic', 'concentration': 13.5, 'benchmark': 10.0, 'unit': 'ug/L', 'half_life_days': 9999, 'koc_L_kg': 120, 'organic_carbon_fraction': 0.01, 'exposure_weight': 0.85, 'monitoring_confidence': 0.88}, {'sample_id': 'ENV003', 'compartment': 'soil', 'analyte': 'lead', 'concentration': 420, 'benchmark': 400, 'unit': 'mg/kg', 'half_life_days': 9999, 'koc_L_kg': 2500, 'organic_carbon_fraction': 0.035, 'exposure_weight': 0.7, 'monitoring_confidence': 0.82}, {'sample_id': 'ENV004', 'compartment': 'sediment', 'analyte': 'pyrene', 'concentration': 1.9, 'benchmark': 1.0, 'unit': 'mg/kg', 'half_life_days': 220, 'koc_L_kg': 60000, 'organic_carbon_fraction': 0.055, 'exposure_weight': 0.45, 'monitoring_confidence': 0.76}, {'sample_id': 'ENV005', 'compartment': 'air', 'analyte': 'ozone', 'concentration': 0.078, 'benchmark': 0.07, 'unit': 'ppm', 'half_life_days': 0.08, 'koc_L_kg': 0, 'organic_carbon_fraction': 0, 'exposure_weight': 0.8, 'monitoring_confidence': 0.9}], 'future': ['multimedia fugacity modeling', 'Monte Carlo uncertainty propagation', 'Bayesian source apportionment', 'exposure pathway graph models', 'spatiotemporal environmental monitoring dashboards'], 'slug': 'environmental-chemistry-chemical-conditions-habitability'}

ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

def parse_value(value):
    if isinstance(value, (int, float)):
        return value
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.upper() == "NA":
        return None
    try:
        return float(text)
    except ValueError:
        return text

def load_rows(path=DATA_FILE):
    rows = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(value) for key, value in row.items()})
    return rows

def write_csv(path, rows):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def ratio_safe(a, b, default=0.0):
    if a is None or b in (None, 0):
        return default
    return a / b

def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))

def log_pressure_ratio(value, reference):
    if value <= 0 or reference <= 0:
        return 0.0
    return math.log1p(value / reference) / math.log(11.0)

def first_order_series(initial, k_per_step, n_steps=40, dt=1.0, label="state"):
    rows = []
    for step in range(n_steps + 1):
        t = step * dt
        value = initial * math.exp(-k_per_step * t)
        rows.append({"step": step, "time": t, label: value, "fraction_remaining": value / initial if initial else 0})
    return rows

def linear_regression(xs, ys):
    n = len(xs)
    if n < 2:
        return {"slope": 0.0, "intercept": ys[0] if ys else 0.0, "n": n}
    mx = mean(xs)
    my = mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom if denom else 0.0
    intercept = my - slope * mx
    return {"slope": slope, "intercept": intercept, "n": n}

def carbonate_fractions(pH, k1=10 ** -6.0, k2=10 ** -9.1):
    h = 10 ** (-pH)
    denom = h * h + k1 * h + k1 * k2
    return {
        "alpha_CO2_star": h * h / denom,
        "alpha_HCO3": k1 * h / denom,
        "alpha_CO3": k1 * k2 / denom,
    }

def isotope_delta(sample_ratio, standard_ratio):
    return ((sample_ratio / standard_ratio) - 1.0) * 1000.0

def radiometric_age_ma(parent, daughter, decay_constant=1.55125e-10):
    if parent <= 0:
        return 0.0
    return (1.0 / decay_constant) * math.log(1.0 + daughter / parent) / 1.0e6

def model_environmental(rows):
    indicators = []
    for row in rows:
        benchmark_ratio = ratio_safe(row["concentration"], row["benchmark"])
        persistence = row["half_life_days"] / (row["half_life_days"] + 30.0)
        partition_retention = ratio_safe(row["koc_L_kg"] * row["organic_carbon_fraction"], 1.0 + row["koc_L_kg"] * row["organic_carbon_fraction"])
        exposure = row["exposure_weight"]
        confidence = row["monitoring_confidence"]
        pressure = clamp(0.38 * log_pressure_ratio(row["concentration"], row["benchmark"]) + 0.22 * persistence + 0.18 * partition_retention + 0.22 * exposure)
        indicators.append({
            **row,
            "benchmark_ratio": benchmark_ratio,
            "persistence_factor": persistence,
            "partition_retention_factor": partition_retention,
            "chemical_habitability_pressure_index": pressure,
            "evidence_weighted_pressure": pressure * confidence,
            "attention_flag": "high_attention" if pressure >= 0.60 else "monitor"
        })
    decay = first_order_series(indicators[0]["concentration"], math.log(2) / max(indicators[0]["half_life_days"], 0.001), 30, 1.0, "concentration")
    return indicators, decay

def model_atmospheric(rows):
    indicators = []
    for row in rows:
        benchmark_ratio = ratio_safe(row["concentration"], row["reference"])
        co2_forcing = 5.35 * math.log(row["concentration"] / row["reference"]) if row["species"] == "CO2" else 0.0
        forcing_proxy = co2_forcing if row["species"] == "CO2" else math.log1p(benchmark_ratio)
        ozone_index = math.sqrt(max(row["nox_ppb"], 0) * max(row["voc_ppb"], 0)) * row["sunlight_index"]
        aerosol_forcing_proxy = -20.0 * row["aod"] * row["single_scattering_albedo"]
        lifetime_factor = row["lifetime_days"] / (row["lifetime_days"] + 30.0)
        pressure = clamp(0.34 * log_pressure_ratio(row["concentration"], row["reference"]) + 0.24 * lifetime_factor + 0.22 * clamp(ozone_index / 100.0) + 0.20 * clamp(abs(aerosol_forcing_proxy) / 5.0))
        indicators.append({
            **row,
            "benchmark_ratio": benchmark_ratio,
            "forcing_proxy": forcing_proxy,
            "ozone_production_index": ozone_index,
            "aerosol_direct_effect_proxy": aerosol_forcing_proxy,
            "atmospheric_chemistry_pressure_index": pressure,
            "attention_flag": "high_attention" if pressure >= 0.60 else "monitor"
        })
    series = first_order_series(rows[1]["concentration"], math.log(2) / rows[1]["lifetime_days"], 36, 30.0, "CH4_ppb")
    return indicators, series

def model_water(rows):
    indicators = []
    for row in rows:
        benchmark_ratio = ratio_safe(row["concentration"], row["benchmark"])
        load_kg_day = row["concentration"] * row["flow_L_s"] * 0.0864 if row["unit"] == "mg/L" else None
        oxygen_deficit = max(row["do_sat_mg_L"] - row["do_obs_mg_L"], 0.0)
        pH_pressure = 1.0 if row["pH"] < 6.5 or row["pH"] > 9.0 else 0.0
        load_pressure = clamp((load_kg_day or 0.0) / 600.0)
        water_quality_pressure = clamp(0.34 * log_pressure_ratio(row["concentration"], row["benchmark"]) + 0.22 * clamp(oxygen_deficit / 5.0) + 0.18 * pH_pressure + 0.16 * load_pressure + 0.10 * (1.0 - row["qc_score"]))
        indicators.append({
            **row,
            "benchmark_ratio": benchmark_ratio,
            "load_kg_day": load_kg_day,
            "oxygen_deficit_mg_L": oxygen_deficit,
            "water_quality_pressure_index": water_quality_pressure,
            "attention_flag": "high_attention" if water_quality_pressure >= 0.50 else "monitor"
        })
    series = first_order_series(100.0, 0.08, 40, 1.0, "storm_pulse_concentration")
    return indicators, series

def model_soil(rows):
    indicators = []
    for row in rows:
        soc_stock = row["soc_percent"] * row["bulk_density_g_cm3"] * row["depth_cm"]
        base_saturation = 100.0 * row["base_cations_cmolc_kg"] / row["cec_cmolc_kg"]
        p_export_kg_ha = row["erosion_t_ha"] * row["sediment_p_mg_kg"] / 1000.0
        nitrate_pressure = clamp(row["nitrate_mg_kg"] / 50.0)
        phosphorus_pressure = clamp(row["phosphorus_mg_kg"] / 120.0)
        acidity_pressure = 1.0 if row["pH"] < 5.8 else 0.0
        soil_pressure = clamp(0.25 * nitrate_pressure + 0.25 * phosphorus_pressure + 0.20 * acidity_pressure + 0.20 * clamp(p_export_kg_ha / 8.0) + 0.10 * (1.0 - clamp(base_saturation / 100.0)))
        indicators.append({
            **row,
            "soc_stock_Mg_ha": soc_stock,
            "base_saturation_percent": base_saturation,
            "phosphorus_export_kg_ha_proxy": p_export_kg_ha,
            "soil_land_system_pressure_index": soil_pressure,
            "attention_flag": "high_attention" if soil_pressure >= 0.50 else "monitor"
        })
    series = []
    soc = rows[0]["soc_percent"]
    for year in range(0, 41):
        soc = soc + 0.015 * (5.0 - soc)
        series.append({"year": year, "modeled_soc_percent": soc, "modeled_soc_stock_Mg_ha": soc * rows[0]["bulk_density_g_cm3"] * rows[0]["depth_cm"]})
    return indicators, series

def model_geochemistry(rows):
    indicators = []
    for row in rows:
        cia = 100.0 * row["Al2O3"] / (row["Al2O3"] + row["CaO"] + row["Na2O"] + row["K2O"])
        rb_sr = ratio_safe(row["Rb_ppm"], row["Sr_ppm"])
        th_u = ratio_safe(row["Th_ppm"], row["U_ppm"])
        age = radiometric_age_ma(row["parent"], row["daughter"])
        delta = isotope_delta(row["sample_ratio"], row["standard_ratio"])
        redox_proxy = row["FeO"] / max(row["SiO2"], 0.001)
        archive_score = clamp(0.30 * clamp(cia / 100.0) + 0.22 * clamp(rb_sr) + 0.20 * clamp(th_u / 5.0) + 0.18 * clamp(redox_proxy) + 0.10 * clamp(abs(delta) / 25.0))
        indicators.append({
            **row,
            "CIA_simplified": cia,
            "Rb_Sr_ratio": rb_sr,
            "Th_U_ratio": th_u,
            "radiometric_age_Ma_simplified": age,
            "delta_notation_permil": delta,
            "redox_archive_proxy": redox_proxy,
            "geochemical_archive_index": archive_score,
            "attention_flag": "strong_archive_signal" if archive_score >= 0.50 else "general_archive_signal"
        })
    series = []
    parent0 = 1.0
    lam = 1.55125e-10
    for ma in range(0, 3001, 100):
        t = ma * 1e6
        parent = parent0 * math.exp(-lam * t)
        series.append({"age_Ma": ma, "parent_fraction": parent, "daughter_fraction": parent0 - parent})
    return indicators, series

def model_ocean(rows):
    indicators = []
    ksp_arag = 6.5e-7
    for row in rows:
        fractions = carbonate_fractions(row["pH"])
        carbonate_umol_kg = fractions["alpha_CO3"] * row["DIC_umol_kg"]
        omega = (row["calcium_mmol_kg"] * 1e-3) * (carbonate_umol_kg * 1e-6) / ksp_arag
        flux_proxy = 0.251 * row["wind_speed_m_s"] ** 2 * (row["pCO2_uatm"] - row["pCO2_air_uatm"])
        buffer_ratio = row["TA_umol_kg"] / row["DIC_umol_kg"]
        acidification_pressure = clamp(0.34 * clamp((8.15 - row["pH"]) / 0.6) + 0.26 * clamp((2.5 - omega) / 2.5) + 0.20 * clamp(abs(flux_proxy) / 8000.0) + 0.20 * clamp((1.15 - buffer_ratio) / 0.2))
        indicators.append({
            **row,
            **fractions,
            "carbonate_umol_kg": carbonate_umol_kg,
            "omega_aragonite_simplified": omega,
            "air_sea_CO2_flux_proxy": flux_proxy,
            "alkalinity_DIC_buffer_ratio": buffer_ratio,
            "ocean_carbonate_pressure_index": acidification_pressure,
            "attention_flag": "low_saturation_attention" if omega < 2.0 else "monitor"
        })
    series = []
    base_dic = rows[0]["DIC_umol_kg"]
    for added in range(0, 401, 20):
        dic = base_dic + added
        pH = rows[0]["pH"] - 0.0009 * added
        fractions = carbonate_fractions(pH)
        carbonate = fractions["alpha_CO3"] * dic
        omega = (rows[0]["calcium_mmol_kg"] * 1e-3) * (carbonate * 1e-6) / ksp_arag
        series.append({"added_DIC_umol_kg": added, "modeled_pH": pH, "modeled_carbonate_umol_kg": carbonate, "modeled_omega_aragonite": omega})
    return indicators, series

def run_model(rows):
    model_type = CONFIG["model_type"]
    if model_type == "environmental":
        return model_environmental(rows)
    if model_type == "atmospheric":
        return model_atmospheric(rows)
    if model_type == "water":
        return model_water(rows)
    if model_type == "soil":
        return model_soil(rows)
    if model_type == "geochemistry":
        return model_geochemistry(rows)
    if model_type == "ocean":
        return model_ocean(rows)
    raise ValueError(f"Unknown model_type: {model_type}")

def summarize(indicators):
    group_key = CONFIG["group_key"]
    groups = {}
    for row in indicators:
        groups.setdefault(row[group_key], []).append(row)

    summary_rows = []
    numeric_keys = [
        key for key, value in indicators[0].items()
        if isinstance(value, (int, float)) and not key.endswith("_id")
    ]

    for group, records in sorted(groups.items()):
        item = {group_key: group, "n": len(records)}
        for key in numeric_keys:
            values = [r[key] for r in records if isinstance(r.get(key), (int, float))]
            if values:
                item[f"mean_{key}"] = mean(values)
                item[f"max_{key}"] = max(values)
        summary_rows.append(item)
    return summary_rows

def write_report(indicators, summary_rows):
    title = CONFIG["title"]
    attention_rows = [row for row in indicators if "attention" in str(row.get("attention_flag", "")) or "strong" in str(row.get("attention_flag", ""))]
    report = [
        f"# Advanced Computational Report: Environmental Chemistry and the Chemical Conditions of Habitability",
        "",
        CONFIG["description"],
        "",
        f"Model type: `{CONFIG['model_type']}`",
        f"Total synthetic records: {len(indicators)}",
        f"Attention records: {len(attention_rows)}",
        "",
        "## Attention records",
        ""
    ]
    for row in attention_rows:
        label = row.get("sample_id", row.get("station", "record"))
        report.append(f"- {label}: {row.get('attention_flag', 'attention')}")
    report.extend(["", "## Group summaries", ""])
    for row in summary_rows:
        report.append("- " + ", ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in row.items()))
    report.extend([
        "",
        "## Responsible use",
        "",
        "These outputs are synthetic educational scaffolds. They are designed to demonstrate computational structure, provenance, and article-specific modeling logic, not to support professional, regulatory, legal, clinical, resource, or operational decisions."
    ])
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)
    (OUT_REPORTS / "advanced_report.md").write_text("\n".join(report), encoding="utf-8")

def write_manifest(indicators, summary_rows):
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": CONFIG["slug"],
        "title": CONFIG["title"],
        "advanced_layer": True,
        "model_type": CONFIG["model_type"],
        "synthetic_records": len(indicators),
        "summary_groups": len(summary_rows),
        "outputs": [
            "advanced/outputs/tables/advanced_indicators.csv",
            "advanced/outputs/tables/advanced_summary.csv",
            "advanced/outputs/tables/advanced_timeseries.csv",
            "advanced/outputs/reports/advanced_report.md"
        ],
        "responsible_use": "Synthetic educational computational layer only."
    }
    (OUT_MANIFESTS / "advanced_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

def main():
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    indicators, series = run_model(rows)
    summary_rows = summarize(indicators)
    write_csv(OUT_TABLES / "advanced_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_summary.csv", summary_rows)
    write_csv(OUT_TABLES / "advanced_timeseries.csv", series)
    write_report(indicators, summary_rows)
    write_manifest(indicators, summary_rows)
    print(f"Advanced workflow complete: {CONFIG['slug']}")
    print(f"Records: {len(indicators)} | Groups: {len(summary_rows)} | Timeseries rows: {len(series)}")

if __name__ == "__main__":
    main()
