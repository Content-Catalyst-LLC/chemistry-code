// Ocean Chemistry and the Carbonate System
// Rust carbonate chemistry screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct OceanRecord {
    region: &'static str,
    water_mass: &'static str,
    p_h: f64,
    alkalinity: f64,
    dic: f64,
    pco2: f64,
    carbonate: f64,
    calcium: f64,
    oxygen: f64,
    nitrate: f64,
    phosphate: f64,
    silicate: f64,
    qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn alkalinity_dic_ratio(r: &OceanRecord) -> f64 {
    if r.dic <= 0.0 { 0.0 } else { r.alkalinity / r.dic }
}

fn buffer_proxy(r: &OceanRecord) -> f64 {
    let p_h_component = clamp01((r.p_h - 7.6) / 0.7);
    let ratio_component = clamp01((alkalinity_dic_ratio(r) - 1.0) / 0.20);
    clamp01(0.55 * p_h_component + 0.45 * ratio_component)
}

fn omega_aragonite(r: &OceanRecord) -> f64 {
    let calcium_umol = r.calcium * 1000.0;
    (r.carbonate * calcium_umol) / (60.0 * 100000.0)
}

fn acidification_pressure(r: &OceanRecord) -> f64 {
    let p_h_component = clamp01((8.2 - r.p_h) / 0.7);
    let co2_component = clamp01((r.pco2 - 400.0) / 800.0);
    let carbonate_component = clamp01((180.0 - r.carbonate) / 180.0);
    let saturation_component = clamp01((3.0 - omega_aragonite(r)) / 3.0);

    clamp01(
        0.30 * p_h_component +
        0.25 * co2_component +
        0.25 * carbonate_component +
        0.20 * saturation_component
    )
}

fn deoxygenation_pressure(r: &OceanRecord) -> f64 {
    clamp01((180.0 - r.oxygen) / 180.0)
}

fn nutrient_upwelling_index(r: &OceanRecord) -> f64 {
    clamp01(
        0.40 * clamp01(r.nitrate / 35.0) +
        0.30 * clamp01(r.phosphate / 3.0) +
        0.30 * clamp01(r.silicate / 60.0)
    )
}

fn carbonate_system_pressure(r: &OceanRecord) -> f64 {
    let qc_penalty = 1.0 - r.qc;

    clamp01(
        0.36 * acidification_pressure(r) +
        0.20 * deoxygenation_pressure(r) +
        0.16 * nutrient_upwelling_index(r) +
        0.18 * (1.0 - buffer_proxy(r)) +
        0.10 * qc_penalty
    )
}

fn flag(r: &OceanRecord) -> &'static str {
    let p = carbonate_system_pressure(r);
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
        OceanRecord { region: "North_Atlantic", water_mass: "surface_subpolar", p_h: 8.08, alkalinity: 2310.0, dic: 2060.0, pco2: 415.0, carbonate: 185.0, calcium: 10.3, oxygen: 255.0, nitrate: 6.2, phosphate: 0.8, silicate: 3.0, qc: 0.94 },
        OceanRecord { region: "Arabian_Sea", water_mass: "oxygen_minimum_zone", p_h: 7.62, alkalinity: 2320.0, dic: 2265.0, pco2: 1050.0, carbonate: 62.0, calcium: 10.2, oxygen: 18.0, nitrate: 38.0, phosphate: 3.2, silicate: 28.0, qc: 0.84 },
        OceanRecord { region: "Caribbean_Reef", water_mass: "surface_tropical", p_h: 8.12, alkalinity: 2380.0, dic: 2040.0, pco2: 390.0, carbonate: 210.0, calcium: 10.5, oxygen: 230.0, nitrate: 0.4, phosphate: 0.2, silicate: 1.0, qc: 0.93 },
    ];

    let mut file = File::create("../outputs/tables/rust_ocean_carbonate_screening.csv")?;
    writeln!(file, "region,water_mass,alkalinity_dic_ratio,buffer_proxy,omega_aragonite,acidification_pressure,deoxygenation_pressure,nutrient_upwelling_index,carbonate_system_pressure,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            record.region,
            record.water_mass,
            alkalinity_dic_ratio(record),
            buffer_proxy(record),
            omega_aragonite(record),
            acidification_pressure(record),
            deoxygenation_pressure(record),
            nutrient_upwelling_index(record),
            carbonate_system_pressure(record),
            flag(record)
        )?;
    }

    println!("Rust ocean carbonate screening complete.");
    Ok(())
}
