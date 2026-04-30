// Water Chemistry and Environmental Monitoring
// Rust water-quality screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Record {
    site: &'static str,
    water_body: &'static str,
    analyte: &'static str,
    concentration: f64,
    benchmark: f64,
    nitrate_mg_l: f64,
    phosphate_mg_l: f64,
    lead_ug_l: f64,
    copper_ug_l: f64,
    arsenic_ug_l: f64,
    dissolved_oxygen_mg_l: f64,
    saturation_mg_l: f64,
    turbidity_ntu: f64,
    qc_score: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn benchmark_ratio(r: &Record) -> f64 {
    if r.benchmark <= 0.0 { 0.0 } else { r.concentration / r.benchmark }
}

fn oxygen_stress(r: &Record) -> f64 {
    let low_do = clamp01((6.0 - r.dissolved_oxygen_mg_l) / 6.0);
    let deficit = clamp01((r.saturation_mg_l - r.dissolved_oxygen_mg_l).max(0.0) / 6.0);
    clamp01(0.60 * low_do + 0.40 * deficit)
}

fn nutrient_index(r: &Record) -> f64 {
    clamp01(0.50 * clamp01(r.nitrate_mg_l / 10.0) +
            0.50 * clamp01(r.phosphate_mg_l / 0.20))
}

fn metal_index(r: &Record) -> f64 {
    clamp01(
        0.34 * clamp01(r.lead_ug_l / 15.0) +
        0.33 * clamp01(r.copper_ug_l / 13.0) +
        0.33 * clamp01(r.arsenic_ug_l / 10.0)
    )
}

fn pressure_index(r: &Record) -> f64 {
    let ratio_component = ((1.0 + benchmark_ratio(r)).ln() / 4.0_f64.ln()).min(1.0);
    let qc_penalty = 1.0 - r.qc_score;

    clamp01(
        0.22 * ratio_component +
        0.18 * oxygen_stress(r) +
        0.20 * nutrient_index(r) +
        0.20 * metal_index(r) +
        0.12 * clamp01(r.turbidity_ntu / 100.0) +
        0.08 * qc_penalty
    )
}

fn flag(r: &Record) -> &'static str {
    let p = pressure_index(r);
    if p >= 0.65 {
        "high_attention"
    } else if p >= 0.45 {
        "moderate_attention"
    } else {
        "monitor"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let records = vec![
        Record { site: "River-A", water_body: "river", analyte: "nitrate_as_N", concentration: 7.8, benchmark: 10.0, nitrate_mg_l: 7.8, phosphate_mg_l: 0.18, lead_ug_l: 3.0, copper_ug_l: 5.0, arsenic_ug_l: 2.5, dissolved_oxygen_mg_l: 8.2, saturation_mg_l: 10.2, turbidity_ntu: 12.0, qc_score: 0.93 },
        Record { site: "Well-C", water_body: "aquifer", analyte: "arsenic", concentration: 12.0, benchmark: 10.0, nitrate_mg_l: 0.2, phosphate_mg_l: 0.02, lead_ug_l: 1.0, copper_ug_l: 2.0, arsenic_ug_l: 12.0, dissolved_oxygen_mg_l: 1.1, saturation_mg_l: 9.8, turbidity_ntu: 0.5, qc_score: 0.86 },
        Record { site: "Storm-D", water_body: "urban_runoff", analyte: "lead", concentration: 18.0, benchmark: 15.0, nitrate_mg_l: 4.5, phosphate_mg_l: 0.42, lead_ug_l: 18.0, copper_ug_l: 21.0, arsenic_ug_l: 3.0, dissolved_oxygen_mg_l: 6.4, saturation_mg_l: 9.1, turbidity_ntu: 75.0, qc_score: 0.80 },
    ];

    let mut file = File::create("../outputs/tables/rust_water_quality_screening.csv")?;
    writeln!(file, "site,water_body,analyte,benchmark_ratio,oxygen_stress,nutrient_index,metal_index,pressure_index,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            record.site,
            record.water_body,
            record.analyte,
            benchmark_ratio(record),
            oxygen_stress(record),
            nutrient_index(record),
            metal_index(record),
            pressure_index(record),
            flag(record)
        )?;
    }

    println!("Rust water quality screening complete.");
    Ok(())
}
