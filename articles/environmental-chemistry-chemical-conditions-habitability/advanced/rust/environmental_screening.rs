// Environmental Chemistry and the Chemical Conditions of Habitability
// Rust environmental chemistry screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Record {
    site: &'static str,
    compartment: &'static str,
    concentration: f64,
    benchmark: f64,
    koc: f64,
    foc: f64,
    half_life_days: f64,
    bulk_density: f64,
    porosity: f64,
    exposure_weight: f64,
    receptor_sensitivity: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn benchmark_ratio(r: &Record) -> f64 {
    if r.benchmark <= 0.0 { 0.0 } else { r.concentration / r.benchmark }
}

fn kd(r: &Record) -> f64 {
    r.koc * r.foc
}

fn retardation(r: &Record) -> f64 {
    let n = r.porosity.max(0.01);
    1.0 + (r.bulk_density * kd(r)) / n
}

fn mobility(r: &Record) -> f64 {
    1.0 / retardation(r).max(1.0).sqrt()
}

fn persistence(r: &Record) -> f64 {
    r.half_life_days / (r.half_life_days + 90.0)
}

fn pressure_index(r: &Record) -> f64 {
    let ratio_component = ((1.0 + benchmark_ratio(r)).ln() / 5.0_f64.ln()).min(1.0);

    clamp01(
        0.34 * ratio_component +
        0.18 * mobility(r) +
        0.18 * persistence(r) +
        0.16 * r.exposure_weight +
        0.14 * r.receptor_sensitivity
    )
}

fn flag(r: &Record) -> &'static str {
    let pressure = pressure_index(r);
    if pressure >= 0.65 {
        "high_attention"
    } else if pressure >= 0.45 {
        "moderate_attention"
    } else {
        "monitor"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let records = vec![
        Record { site: "Groundwater-B", compartment: "groundwater", concentration: 13.5, benchmark: 10.0, koc: 120.0, foc: 0.002, half_life_days: 99999.0, bulk_density: 1.65, porosity: 0.32, exposure_weight: 0.95, receptor_sensitivity: 0.90 },
        Record { site: "Sediment-D", compartment: "sediment", concentration: 1.9, benchmark: 1.0, koc: 60000.0, foc: 0.055, half_life_days: 220.0, bulk_density: 1.15, porosity: 0.58, exposure_weight: 0.55, receptor_sensitivity: 0.82 },
        Record { site: "Groundwater-I", compartment: "groundwater", concentration: 8.5, benchmark: 5.0, koc: 90.0, foc: 0.001, half_life_days: 365.0, bulk_density: 1.70, porosity: 0.30, exposure_weight: 0.93, receptor_sensitivity: 0.91 },
    ];

    let mut file = File::create("../outputs/tables/rust_environmental_screening.csv")?;
    writeln!(file, "site,compartment,benchmark_ratio,Kd_L_kg,retardation_factor,mobility_factor,persistence_factor,pressure_index,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            record.site,
            record.compartment,
            benchmark_ratio(record),
            kd(record),
            retardation(record),
            mobility(record),
            persistence(record),
            pressure_index(record),
            flag(record)
        )?;
    }

    println!("Rust environmental screening complete.");
    Ok(())
}
