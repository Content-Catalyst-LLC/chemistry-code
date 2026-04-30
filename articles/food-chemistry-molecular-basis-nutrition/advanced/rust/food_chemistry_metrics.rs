// Food Chemistry and the Molecular Basis of Nutrition
// Rust food chemistry scoring example.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Food {
    name: &'static str,
    energy_kcal: f64,
    protein_g: f64,
    fiber_g: f64,
    potassium_mg: f64,
    starch_g: f64,
    sugars_g: f64,
    particle_accessibility: f64,
    processing_intensity: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn nutrient_density(food: &Food) -> f64 {
    let beneficial =
        0.40 * clamp01(food.protein_g / 25.0) +
        0.35 * clamp01(food.fiber_g / 12.0) +
        0.25 * clamp01(food.potassium_mg / 800.0);

    let energy_factor = (food.energy_kcal / 100.0).max(0.5);
    beneficial / energy_factor
}

fn glycemic_accessibility(food: &Food) -> f64 {
    let fiber_protection = clamp01(food.fiber_g / 12.0);

    clamp01(
        0.32 * clamp01(food.starch_g / 30.0) +
        0.24 * clamp01(food.sugars_g / 20.0) +
        0.22 * food.particle_accessibility +
        0.16 * food.processing_intensity -
        0.20 * fiber_protection
    )
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let foods = vec![
        Food { name: "lentils_cooked", energy_kcal: 230.0, protein_g: 18.0, fiber_g: 15.0, potassium_mg: 730.0, starch_g: 22.0, sugars_g: 3.0, particle_accessibility: 0.45, processing_intensity: 0.25 },
        Food { name: "white_bread", energy_kcal: 160.0, protein_g: 5.0, fiber_g: 1.0, potassium_mg: 70.0, starch_g: 24.0, sugars_g: 3.0, particle_accessibility: 0.88, processing_intensity: 0.75 },
        Food { name: "oats_cooked", energy_kcal: 180.0, protein_g: 10.0, fiber_g: 8.0, potassium_mg: 180.0, starch_g: 18.0, sugars_g: 1.0, particle_accessibility: 0.50, processing_intensity: 0.30 },
    ];

    let mut file = File::create("../outputs/tables/rust_food_chemistry_metrics.csv")?;
    writeln!(file, "food,nutrient_density,glycemic_accessibility")?;

    for food in &foods {
        writeln!(
            file,
            "{},{:.6},{:.6}",
            food.name,
            nutrient_density(food),
            glycemic_accessibility(food)
        )?;
    }

    println!("Rust food chemistry metrics complete.");
    Ok(())
}
