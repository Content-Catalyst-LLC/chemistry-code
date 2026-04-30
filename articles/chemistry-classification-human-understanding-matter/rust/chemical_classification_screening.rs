// Chemistry, Classification, and the Human Understanding of Matter
// Rust chemical classification screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Record {
    sample_name: &'static str,
    components: f64,
    phase: &'static str,
    contains_metal: bool,
    coordination_number: f64,
    is_polymer: bool,
    network_structure: bool,
    organic_fraction: f64,
    ionic_fraction: f64,
    metallic_fraction: f64,
    crystalline_score: f64,
    functional_group: &'static str,
    spectral: f64,
    elemental: f64,
    thermal: f64,
    confidence: f64,
    qc: f64,
    hazard: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn assign_class(r: &Record) -> &'static str {
    if r.components > 3.0 {
        if r.phase == "heterogeneous_mixture" {
            "heterogeneous_mixture"
        } else {
            "mixture_or_solution"
        }
    } else if r.is_polymer {
        "polymer_material"
    } else if r.contains_metal && r.coordination_number >= 4.0 && r.functional_group == "coordination_complex" {
        "coordination_compound"
    } else if r.ionic_fraction >= 0.65 && r.crystalline_score >= 0.65 {
        "ionic_or_salt_crystal"
    } else if r.network_structure && (r.phase == "crystalline_solid" || r.phase == "amorphous_solid") {
        "extended_solid_or_network_material"
    } else if r.organic_fraction >= 0.65 {
        "organic_molecular_substance"
    } else if r.metallic_fraction >= 0.40 {
        "metallic_or_intermetallic_material"
    } else {
        "molecular_or_material_record"
    }
}

fn evidence_score(r: &Record) -> f64 {
    clamp01(0.35 * r.spectral + 0.30 * r.elemental + 0.20 * r.thermal + 0.15 * r.qc)
}

fn reliability(r: &Record) -> f64 {
    clamp01(0.55 * evidence_score(r) + 0.30 * r.confidence + 0.15 * r.qc)
}

fn hazard_triage(r: &Record) -> &'static str {
    if r.hazard >= 0.60 {
        "higher_attention"
    } else if r.hazard >= 0.35 {
        "moderate_attention"
    } else {
        "lower_attention"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let records = vec![
        Record { sample_name: "ethyl_acetate_reference", components: 1.0, phase: "liquid", contains_metal: false, coordination_number: 0.0, is_polymer: false, network_structure: false, organic_fraction: 1.0, ionic_fraction: 0.0, metallic_fraction: 0.0, crystalline_score: 0.05, functional_group: "ester", spectral: 0.92, elemental: 0.88, thermal: 0.74, confidence: 0.86, qc: 0.94, hazard: 0.22 },
        Record { sample_name: "sodium_chloride_crystal", components: 2.0, phase: "crystalline_solid", contains_metal: true, coordination_number: 6.0, is_polymer: false, network_structure: true, organic_fraction: 0.0, ionic_fraction: 0.95, metallic_fraction: 0.0, crystalline_score: 0.96, functional_group: "halide_salt", spectral: 0.88, elemental: 0.93, thermal: 0.70, confidence: 0.91, qc: 0.96, hazard: 0.18 },
        Record { sample_name: "soil_extract", components: 60.0, phase: "heterogeneous_mixture", contains_metal: true, coordination_number: 0.0, is_polymer: false, network_structure: true, organic_fraction: 0.30, ionic_fraction: 0.50, metallic_fraction: 0.05, crystalline_score: 0.42, functional_group: "mixed_matrix", spectral: 0.48, elemental: 0.72, thermal: 0.55, confidence: 0.60, qc: 0.82, hazard: 0.62 },
    ];

    let mut file = File::create("../outputs/tables/rust_chemical_classification_screening.csv")?;
    writeln!(file, "sample_name,assigned_class,evidence_score,classification_reliability,hazard_triage")?;

    for r in &records {
        writeln!(
            file,
            "{},{},{:.6},{:.6},{}",
            r.sample_name,
            assign_class(r),
            evidence_score(r),
            reliability(r),
            hazard_triage(r)
        )?;
    }

    println!("Rust chemical classification screening complete.");
    Ok(())
}
