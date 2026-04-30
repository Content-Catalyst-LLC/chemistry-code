// Astrochemistry and the Molecular Universe
// Rust astrochemical screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct AstroRecord {
    region: &'static str,
    environment: &'static str,
    family: &'static str,
    species: &'static str,
    density: f64,
    column_density: f64,
    uv_field: f64,
    cosmic_ray: f64,
    visual_extinction: f64,
    binding_energy: f64,
    dust_temp: f64,
    photo_rate: f64,
    ice_fraction: f64,
    water_ice_index: f64,
    organic_complexity: f64,
    deuteration: f64,
    metallicity: f64,
    qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn uv_attenuation(r: &AstroRecord) -> f64 {
    r.uv_field * (-1.8 * r.visual_extinction).exp()
}

fn attenuated_photo_rate(r: &AstroRecord) -> f64 {
    r.photo_rate * uv_attenuation(r)
}

fn freezeout_efficiency(r: &AstroRecord) -> f64 {
    let density_component = clamp01(r.density.max(1.0).log10() / 8.0);
    let thermal_retention = clamp01(r.binding_energy / (100.0 * r.dust_temp).max(1.0));
    clamp01(0.55 * density_component + 0.45 * thermal_retention)
}

fn ionization_pressure(r: &AstroRecord) -> f64 {
    clamp01((r.cosmic_ray.max(1e-20) / 1e-18).log10() / 4.0)
}

fn molecular_complexity_score(r: &AstroRecord) -> f64 {
    let column_component = clamp01(r.column_density.max(1.0).log10() / 18.0);
    clamp01(0.45 * r.organic_complexity + 0.35 * column_component + 0.20 * r.metallicity)
}

fn ice_chemistry_score(r: &AstroRecord) -> f64 {
    clamp01(0.40 * r.ice_fraction + 0.35 * r.water_ice_index + 0.25 * freezeout_efficiency(r))
}

fn activity_index(r: &AstroRecord) -> f64 {
    let qc_penalty = 1.0 - r.qc;
    clamp01(
        0.20 * molecular_complexity_score(r) +
        0.19 * ice_chemistry_score(r) +
        0.18 * ionization_pressure(r) +
        0.15 * freezeout_efficiency(r) +
        0.12 * r.deuteration +
        0.08 * qc_penalty -
        0.12 * clamp01(attenuated_photo_rate(r) / 1e-8)
    )
}

fn flag(r: &AstroRecord) -> &'static str {
    let a = activity_index(r);
    if a >= 0.65 {
        "high_activity"
    } else if a >= 0.45 {
        "moderate_activity"
    } else {
        "low_to_monitor"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let records = vec![
        AstroRecord { region: "Taurus_TMC1", environment: "cold_dark_cloud", family: "carbon_chain", species: "HC3N", density: 120000.0, column_density: 2.2e13, uv_field: 0.05, cosmic_ray: 1.3e-17, visual_extinction: 12.0, binding_energy: 3600.0, dust_temp: 8.0, photo_rate: 1.0e-11, ice_fraction: 0.72, water_ice_index: 0.65, organic_complexity: 0.54, deuteration: 0.08, metallicity: 1.00, qc: 0.93 },
        AstroRecord { region: "Orion_KL", environment: "hot_core", family: "complex_organic", species: "CH3OCH3", density: 5000000.0, column_density: 8.0e15, uv_field: 10.0, cosmic_ray: 5.0e-16, visual_extinction: 8.0, binding_energy: 4200.0, dust_temp: 120.0, photo_rate: 3.0e-10, ice_fraction: 0.35, water_ice_index: 0.42, organic_complexity: 0.92, deuteration: 0.03, metallicity: 1.15, qc: 0.90 },
        AstroRecord { region: "TW_Hya", environment: "disk_midplane", family: "ice_chemistry", species: "H2O_ice", density: 100000000.0, column_density: 1.0e18, uv_field: 0.20, cosmic_ray: 1.0e-17, visual_extinction: 20.0, binding_energy: 5700.0, dust_temp: 18.0, photo_rate: 1.0e-12, ice_fraction: 0.88, water_ice_index: 0.95, organic_complexity: 0.30, deuteration: 0.12, metallicity: 1.00, qc: 0.91 },
    ];

    let mut file = File::create("../outputs/tables/rust_astrochemistry_screening.csv")?;
    writeln!(file, "region,environment,family,species,uv_attenuation,attenuated_photo_rate,freezeout_efficiency,ionization_pressure,molecular_complexity_score,ice_chemistry_score,activity_index,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{},{},{:.12e},{:.12e},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            record.region,
            record.environment,
            record.family,
            record.species,
            uv_attenuation(record),
            attenuated_photo_rate(record),
            freezeout_efficiency(record),
            ionization_pressure(record),
            molecular_complexity_score(record),
            ice_chemistry_score(record),
            activity_index(record),
            flag(record)
        )?;
    }

    println!("Rust astrochemistry screening complete.");
    Ok(())
}
