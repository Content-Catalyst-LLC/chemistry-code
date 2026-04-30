// Geochemistry and the Chemical History of Earth
// Rust geochemical screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Sample {
    sample_id: &'static str,
    province: &'static str,
    rock_type: &'static str,
    parent_isotope: &'static str,
    reported_age_ma: f64,
    parent_fraction: f64,
    sio2: f64,
    al2o3: f64,
    cao: f64,
    na2o: f64,
    k2o: f64,
    mgo: f64,
    feo: f64,
    mno: f64,
    tio2: f64,
    rb: f64,
    sr: f64,
    epsilon_nd: f64,
    initial_sr: f64,
    redox_proxy: f64,
    qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn half_life_ma(parent: &str) -> f64 {
    match parent {
        "Rb87" => 48800.0,
        "Sm147" => 106000.0,
        "K40" => 1250.0,
        "U238" => 4468.0,
        _ => 0.0,
    }
}

fn model_age(sample: &Sample) -> f64 {
    let half_life = half_life_ma(sample.parent_isotope);
    if sample.parent_fraction <= 0.0 || sample.parent_fraction > 1.0 || half_life <= 0.0 {
        0.0
    } else {
        -sample.parent_fraction.ln() / (std::f64::consts::LN_2 / half_life)
    }
}

fn cia(sample: &Sample) -> f64 {
    let denominator = sample.al2o3 + sample.cao + sample.na2o + sample.k2o;
    if denominator <= 0.0 { 0.0 } else { 100.0 * sample.al2o3 / denominator }
}

fn mafic_index(sample: &Sample) -> f64 {
    let mafic = sample.mgo + sample.feo + sample.tio2;
    let total = mafic + sample.sio2;
    if total <= 0.0 { 0.0 } else { mafic / total }
}

fn crustal_evolution(sample: &Sample) -> f64 {
    let silica = clamp01((sample.sio2 - 45.0) / 30.0);
    let rb_sr = sample.rb / sample.sr.max(0.001);
    let evolved_sr = clamp01((sample.initial_sr - 0.703) / 0.020);
    let depleted_mantle = clamp01((sample.epsilon_nd + 5.0) / 15.0);

    clamp01(0.35 * silica + 0.25 * clamp01(rb_sr / 1.5) + 0.25 * evolved_sr + 0.15 * (1.0 - depleted_mantle))
}

fn redox_state(sample: &Sample) -> f64 {
    clamp01(0.65 * sample.redox_proxy + 0.25 * clamp01(sample.feo / 15.0) + 0.10 * clamp01(sample.mno / 0.30))
}

fn geochemical_pressure(sample: &Sample) -> f64 {
    let age = model_age(sample);
    let age_disagreement = ((age - sample.reported_age_ma).abs() / sample.reported_age_ma.max(1.0)).min(1.0);
    let weathering = clamp01((cia(sample) - 50.0) / 50.0);
    let qc_penalty = 1.0 - sample.qc;

    clamp01(
        0.18 * age_disagreement +
        0.18 * weathering +
        0.16 * mafic_index(sample) +
        0.18 * crustal_evolution(sample) +
        0.18 * redox_state(sample) +
        0.12 * qc_penalty
    )
}

fn flag(sample: &Sample) -> &'static str {
    let p = geochemical_pressure(sample);
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

    let samples = vec![
        Sample { sample_id: "GEOFS001", province: "Superior_Craton", rock_type: "granite", parent_isotope: "Rb87", reported_age_ma: 2700.0, parent_fraction: 0.72, sio2: 72.5, al2o3: 14.1, cao: 1.8, na2o: 3.4, k2o: 4.8, mgo: 0.6, feo: 1.9, mno: 0.04, tio2: 0.31, rb: 185.0, sr: 210.0, epsilon_nd: -6.2, initial_sr: 0.7125, redox_proxy: 0.32, qc: 0.93 },
        Sample { sample_id: "GEOFS006", province: "Banded_Iron_Formation", rock_type: "iron_formation", parent_isotope: "U238", reported_age_ma: 2400.0, parent_fraction: 0.61, sio2: 38.0, al2o3: 2.5, cao: 3.2, na2o: 0.1, k2o: 0.05, mgo: 2.8, feo: 42.0, mno: 0.25, tio2: 0.2, rb: 1.0, sr: 22.0, epsilon_nd: -1.0, initial_sr: 0.7040, redox_proxy: 0.92, qc: 0.86 },
    ];

    let mut file = File::create("../outputs/tables/rust_geochemistry_screening.csv")?;
    writeln!(file, "sample_id,province,rock_type,parent_isotope,model_age_ma,CIA,mafic_index,crustal_evolution_proxy,redox_state_proxy,geochemical_pressure,flag")?;

    for sample in &samples {
        writeln!(
            file,
            "{},{},{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            sample.sample_id,
            sample.province,
            sample.rock_type,
            sample.parent_isotope,
            model_age(sample),
            cia(sample),
            mafic_index(sample),
            crustal_evolution(sample),
            redox_state(sample),
            geochemical_pressure(sample),
            flag(sample)
        )?;
    }

    println!("Rust geochemistry screening complete.");
    Ok(())
}
