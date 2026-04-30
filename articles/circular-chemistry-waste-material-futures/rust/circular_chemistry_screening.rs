// Circular Chemistry, Waste, and Material Futures
// Rust circular chemistry screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Stream {
    name: &'static str,
    material_class: &'static str,
    pathway: &'static str,
    input_kg: f64,
    recovered_kg: f64,
    quality: f64,
    substitution: f64,
    energy: f64,
    reagent: f64,
    hazard: f64,
    exposure: f64,
    contamination: f64,
    traceability: f64,
    collection: f64,
    sorting: f64,
    worker_exposure: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn recovery_yield(s: &Stream) -> f64 {
    if s.input_kg <= 0.0 { 0.0 } else { s.recovered_kg / s.input_kg }
}

fn circular_retention(s: &Stream) -> f64 {
    recovery_yield(s) * s.quality * s.substitution
}

fn safe_circularity(s: &Stream) -> f64 {
    clamp01(
        0.30 * (1.0 - s.hazard) +
        0.25 * (1.0 - s.exposure) +
        0.25 * (1.0 - s.contamination) +
        0.20 * (1.0 - s.worker_exposure)
    )
}

fn infrastructure(s: &Stream) -> f64 {
    clamp01(0.45 * s.collection + 0.40 * s.sorting + 0.15 * s.traceability)
}

fn energy_score(s: &Stream) -> f64 {
    if s.recovered_kg <= 0.0 {
        0.0
    } else {
        clamp01(1.0 - (s.energy / s.recovered_kg) / 2.0)
    }
}

fn reagent_score(s: &Stream) -> f64 {
    if s.recovered_kg <= 0.0 {
        0.0
    } else {
        clamp01(1.0 - (s.reagent / s.recovered_kg) / 0.6)
    }
}

fn circular_score(s: &Stream) -> f64 {
    clamp01(
        0.18 * recovery_yield(s) +
        0.22 * circular_retention(s) +
        0.16 * safe_circularity(s) +
        0.14 * infrastructure(s) +
        0.12 * energy_score(s) +
        0.08 * reagent_score(s) +
        0.10 * s.traceability
    )
}

fn flag(s: &Stream) -> &'static str {
    let score = circular_score(s);
    if score >= 0.70 {
        "strong_circular_profile"
    } else if score >= 0.50 {
        "moderate_profile_with_constraints"
    } else {
        "redesign_or_infrastructure_priority"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let streams = vec![
        Stream { name: "PET_bottles_clear", material_class: "polymer", pathway: "mechanical_recycling", input_kg: 1000.0, recovered_kg: 760.0, quality: 0.82, substitution: 0.72, energy: 180.0, reagent: 12.0, hazard: 0.18, exposure: 0.22, contamination: 0.18, traceability: 0.78, collection: 0.68, sorting: 0.74, worker_exposure: 0.20 },
        Stream { name: "Lithium_ion_batteries", material_class: "battery", pathway: "hydrometallurgical_recovery", input_kg: 500.0, recovered_kg: 310.0, quality: 0.78, substitution: 0.72, energy: 520.0, reagent: 160.0, hazard: 0.48, exposure: 0.55, contamination: 0.40, traceability: 0.70, collection: 0.52, sorting: 0.64, worker_exposure: 0.58 },
        Stream { name: "Solvent_wash_stream", material_class: "solvent", pathway: "distillation_recovery", input_kg: 1500.0, recovered_kg: 1260.0, quality: 0.88, substitution: 0.86, energy: 340.0, reagent: 20.0, hazard: 0.32, exposure: 0.46, contamination: 0.20, traceability: 0.75, collection: 0.80, sorting: 0.90, worker_exposure: 0.42 },
    ];

    let mut file = File::create("../outputs/tables/rust_circular_chemistry_screening.csv")?;
    writeln!(file, "stream,material_class,pathway,recovery_yield,circular_retention,safe_circularity,infrastructure,energy_score,reagent_score,circular_score,flag")?;

    for s in &streams {
        writeln!(
            file,
            "{},{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            s.name,
            s.material_class,
            s.pathway,
            recovery_yield(s),
            circular_retention(s),
            safe_circularity(s),
            infrastructure(s),
            energy_score(s),
            reagent_score(s),
            circular_score(s),
            flag(s)
        )?;
    }

    println!("Rust circular chemistry screening complete.");
    Ok(())
}
