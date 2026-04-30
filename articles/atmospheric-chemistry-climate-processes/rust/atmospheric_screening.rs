// Atmospheric Chemistry and Climate Processes
// Rust atmospheric chemistry screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Record {
    station: &'static str,
    species: &'static str,
    chemical_class: &'static str,
    concentration: f64,
    reference: f64,
    nox_ppb: f64,
    voc_ppb: f64,
    sunlight: f64,
    aod: f64,
    ssa: f64,
    lifetime_days: f64,
    qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn reference_ratio(r: &Record) -> f64 {
    if r.reference <= 0.0 { 0.0 } else { r.concentration / r.reference }
}

fn greenhouse_forcing(r: &Record) -> f64 {
    if r.concentration <= 0.0 || r.reference <= 0.0 {
        return 0.0;
    }

    match r.species {
        "CO2" => 5.35 * (r.concentration / r.reference).ln(),
        "CH4" => 0.036 * (r.concentration.sqrt() - r.reference.sqrt()),
        "N2O" => 0.12 * (r.concentration.sqrt() - r.reference.sqrt()),
        _ => 0.0,
    }
}

fn ozone_index(r: &Record) -> f64 {
    if r.nox_ppb <= 0.0 || r.voc_ppb <= 0.0 {
        0.0
    } else {
        (r.nox_ppb * r.voc_ppb).sqrt() * r.sunlight
    }
}

fn aerosol_effect(r: &Record) -> f64 {
    -25.0 * r.aod * r.ssa + 12.0 * r.aod * (1.0 - r.ssa)
}

fn persistence(r: &Record) -> f64 {
    r.lifetime_days / (r.lifetime_days + 30.0)
}

fn pressure_index(r: &Record) -> f64 {
    let ratio_component = ((1.0 + reference_ratio(r)).ln() / 4.0_f64.ln()).min(1.0);
    let forcing_component = clamp01(greenhouse_forcing(r).abs() / 4.0);
    let ozone_component = clamp01(ozone_index(r) / 100.0);
    let aerosol_component = clamp01(aerosol_effect(r).abs() / 20.0);
    let qc_penalty = 1.0 - r.qc;

    if r.chemical_class == "greenhouse_gas" {
        clamp01(0.28 * ratio_component + 0.34 * forcing_component + 0.25 * persistence(r) + 0.08 * ozone_component + 0.05 * qc_penalty)
    } else if r.chemical_class == "aerosol" {
        clamp01(0.24 * ratio_component + 0.34 * aerosol_component + 0.18 * persistence(r) + 0.14 * ozone_component + 0.10 * qc_penalty)
    } else {
        clamp01(0.26 * ratio_component + 0.36 * ozone_component + 0.14 * aerosol_component + 0.14 * persistence(r) + 0.10 * qc_penalty)
    }
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
        Record { station: "Global-CO2", species: "CO2", chemical_class: "greenhouse_gas", concentration: 423.0, reference: 280.0, nox_ppb: 0.0, voc_ppb: 0.0, sunlight: 1.0, aod: 0.04, ssa: 0.96, lifetime_days: 36500.0, qc: 0.95 },
        Record { station: "Urban-O3", species: "O3", chemical_class: "secondary_pollutant", concentration: 0.078, reference: 0.070, nox_ppb: 38.0, voc_ppb: 85.0, sunlight: 1.15, aod: 0.08, ssa: 0.93, lifetime_days: 0.20, qc: 0.90 },
        Record { station: "Wildfire-PM", species: "PM2.5", chemical_class: "aerosol", concentration: 38.0, reference: 15.0, nox_ppb: 22.0, voc_ppb: 95.0, sunlight: 0.75, aod: 0.68, ssa: 0.86, lifetime_days: 5.0, qc: 0.84 },
    ];

    let mut file = File::create("../outputs/tables/rust_atmospheric_screening.csv")?;
    writeln!(file, "station,species,chemical_class,reference_ratio,forcing_proxy,ozone_index,aerosol_effect,persistence_factor,pressure_index,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            record.station,
            record.species,
            record.chemical_class,
            reference_ratio(record),
            greenhouse_forcing(record),
            ozone_index(record),
            aerosol_effect(record),
            persistence(record),
            pressure_index(record),
            flag(record)
        )?;
    }

    println!("Rust atmospheric screening complete.");
    Ok(())
}
