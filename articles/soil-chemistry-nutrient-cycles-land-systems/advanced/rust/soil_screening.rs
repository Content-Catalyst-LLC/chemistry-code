// Soil Chemistry, Nutrient Cycles, and Land Systems
// Rust soil chemistry screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct SoilRecord {
    site: &'static str,
    land_use: &'static str,
    pH: f64,
    organic_matter: f64,
    cec: f64,
    nitrate: f64,
    ammonium: f64,
    available_p: f64,
    exchangeable_k: f64,
    ec: f64,
    sar: f64,
    clay: f64,
    sand: f64,
    rainfall: f64,
    erosion: f64,
    compaction: f64,
    qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn ph_stress(p_h: f64) -> f64 {
    if p_h < 6.0 {
        clamp01((6.0 - p_h) / 2.0)
    } else if p_h > 7.8 {
        clamp01((p_h - 7.8) / 2.0)
    } else {
        0.0
    }
}

fn nutrient_balance(r: &SoilRecord) -> f64 {
    let nitrogen = clamp01((r.nitrate + r.ammonium) / 60.0);
    let phosphorus = clamp01(r.available_p / 40.0);
    let potassium = clamp01(r.exchangeable_k / 250.0);
    clamp01(0.40 * nitrogen + 0.30 * phosphorus + 0.30 * potassium)
}

fn salinity_sodicity(r: &SoilRecord) -> f64 {
    let salinity = clamp01((r.ec - 2.0) / 6.0);
    let sodicity = clamp01((r.sar - 6.0) / 12.0);
    salinity.max(sodicity)
}

fn organic_score(r: &SoilRecord) -> f64 {
    clamp01(r.organic_matter / 6.0)
}

fn cec_score(r: &SoilRecord) -> f64 {
    clamp01(r.cec / 25.0)
}

fn leaching_pressure(r: &SoilRecord) -> f64 {
    let buffering = 0.5 * organic_score(r) + 0.5 * cec_score(r);
    clamp01(0.40 * r.sand + 0.35 * r.rainfall + 0.25 * clamp01(r.nitrate / 50.0) - 0.25 * buffering)
}

fn carbon_stability(r: &SoilRecord) -> f64 {
    clamp01(0.45 * r.clay + 0.40 * organic_score(r) + 0.15 * (1.0 - r.erosion))
}

fn soil_pressure(r: &SoilRecord) -> f64 {
    clamp01(
        0.18 * (1.0 - nutrient_balance(r)) +
        0.18 * leaching_pressure(r) +
        0.16 * salinity_sodicity(r) +
        0.14 * ph_stress(r.pH) +
        0.14 * r.erosion +
        0.10 * r.compaction +
        0.07 * (1.0 - carbon_stability(r)) +
        0.03 * (1.0 - r.qc)
    )
}

fn flag(r: &SoilRecord) -> &'static str {
    let p = soil_pressure(r);
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
        SoilRecord { site: "Prairie-A", land_use: "cropland", pH: 6.4, organic_matter: 4.8, cec: 22.0, nitrate: 18.0, ammonium: 6.0, available_p: 28.0, exchangeable_k: 190.0, ec: 0.8, sar: 2.0, clay: 0.34, sand: 0.28, rainfall: 0.55, erosion: 0.22, compaction: 0.18, qc: 0.94 },
        SoilRecord { site: "Irrigated-C", land_use: "irrigated_agriculture", pH: 8.2, organic_matter: 1.6, cec: 14.0, nitrate: 25.0, ammonium: 5.0, available_p: 32.0, exchangeable_k: 210.0, ec: 5.8, sar: 12.0, clay: 0.22, sand: 0.44, rainfall: 0.40, erosion: 0.30, compaction: 0.25, qc: 0.86 },
        SoilRecord { site: "Degraded-E", land_use: "degraded_land", pH: 5.1, organic_matter: 0.9, cec: 5.0, nitrate: 8.0, ammonium: 2.0, available_p: 5.0, exchangeable_k: 70.0, ec: 2.2, sar: 8.0, clay: 0.10, sand: 0.72, rainfall: 0.80, erosion: 0.82, compaction: 0.65, qc: 0.78 },
    ];

    let mut file = File::create("../outputs/tables/rust_soil_screening.csv")?;
    writeln!(file, "site,land_use,pH_stress,nutrient_balance,leaching_pressure,salinity_sodicity,carbon_stability,soil_pressure,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            record.site,
            record.land_use,
            ph_stress(record.pH),
            nutrient_balance(record),
            leaching_pressure(record),
            salinity_sodicity(record),
            carbon_stability(record),
            soil_pressure(record),
            flag(record)
        )?;
    }

    println!("Rust soil screening complete.");
    Ok(())
}
