// Toxicology, Exposure, and Chemical Risk
// Rust exposure screening and risk indexing.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Exposure {
    chemical: &'static str,
    medium: &'static str,
    route: &'static str,
    concentration: f64,
    intake_rate: f64,
    exposure_frequency: f64,
    exposure_duration: f64,
    body_weight: f64,
    averaging_time: f64,
    absorption_fraction: f64,
    reference_dose: f64,
    vulnerability_factor: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn chronic_daily_intake(e: &Exposure) -> f64 {
    if e.body_weight <= 0.0 || e.averaging_time <= 0.0 {
        0.0
    } else {
        e.concentration * e.intake_rate * e.exposure_frequency * e.exposure_duration
            / (e.body_weight * e.averaging_time)
    }
}

fn absorbed_dose(e: &Exposure) -> f64 {
    chronic_daily_intake(e) * e.absorption_fraction
}

fn hazard_quotient(e: &Exposure) -> f64 {
    if e.reference_dose <= 0.0 {
        0.0
    } else {
        absorbed_dose(e) / e.reference_dose
    }
}

fn vulnerability_adjusted_hazard(e: &Exposure) -> f64 {
    hazard_quotient(e) * e.vulnerability_factor
}

fn screening_index(e: &Exposure) -> f64 {
    let hq = hazard_quotient(e);
    let hq_component = ((1.0 + hq).ln() / 11.0_f64.ln()).min(1.0);
    let vulnerability_component = clamp01((e.vulnerability_factor - 1.0) / 1.0);
    clamp01(0.70 * hq_component + 0.30 * vulnerability_component)
}

fn flag(e: &Exposure) -> &'static str {
    if hazard_quotient(e) >= 1.0 || screening_index(e) >= 0.65 {
        "high_attention"
    } else if hazard_quotient(e) >= 0.3 || screening_index(e) >= 0.45 {
        "moderate_attention"
    } else {
        "monitor"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let records = vec![
        Exposure { chemical: "arsenic", medium: "drinking_water", route: "ingestion", concentration: 0.010, intake_rate: 2.0, exposure_frequency: 350.0, exposure_duration: 30.0, body_weight: 70.0, averaging_time: 10950.0, absorption_fraction: 0.95, reference_dose: 0.0003, vulnerability_factor: 1.2 },
        Exposure { chemical: "lead", medium: "soil_dust", route: "ingestion", concentration: 120.0, intake_rate: 0.0001, exposure_frequency: 180.0, exposure_duration: 6.0, body_weight: 15.0, averaging_time: 2190.0, absorption_fraction: 0.40, reference_dose: 0.0035, vulnerability_factor: 1.8 },
        Exposure { chemical: "PFOS", medium: "drinking_water", route: "ingestion", concentration: 0.000020, intake_rate: 2.0, exposure_frequency: 350.0, exposure_duration: 30.0, body_weight: 70.0, averaging_time: 10950.0, absorption_fraction: 0.90, reference_dose: 0.00000002, vulnerability_factor: 1.35 },
    ];

    let mut file = File::create("../outputs/tables/rust_toxicology_screening.csv")?;
    writeln!(file, "chemical,medium,route,cdi,absorbed_dose,hazard_quotient,vulnerability_adjusted_hazard,screening_index,flag")?;

    for record in &records {
        writeln!(
            file,
            "{},{},{},{:.10},{:.10},{:.6},{:.6},{:.6},{}",
            record.chemical,
            record.medium,
            record.route,
            chronic_daily_intake(record),
            absorbed_dose(record),
            hazard_quotient(record),
            vulnerability_adjusted_hazard(record),
            screening_index(record),
            flag(record)
        )?;
    }

    println!("Rust toxicology screening complete.");
    Ok(())
}
