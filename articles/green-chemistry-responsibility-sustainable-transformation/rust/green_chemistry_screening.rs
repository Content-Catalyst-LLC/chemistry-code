// Green Chemistry, Responsibility, and Sustainable Transformation
// Rust green chemistry screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Route {
    route_name: &'static str,
    chemistry_class: &'static str,
    product_mass: f64,
    product_mw: f64,
    reactant_mw_sum: f64,
    total_input_mass: f64,
    waste_mass: f64,
    solvent_mass: f64,
    energy_kwh: f64,
    catalyst_loading: f64,
    hazard_score: f64,
    solvent_hazard_score: f64,
    renewable: f64,
    circularity: f64,
    degradation: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn atom_economy(r: &Route) -> f64 {
    if r.reactant_mw_sum <= 0.0 { 0.0 } else { r.product_mw / r.reactant_mw_sum }
}

fn e_factor(r: &Route) -> f64 {
    if r.product_mass <= 0.0 { 0.0 } else { r.waste_mass / r.product_mass }
}

fn pmi(r: &Route) -> f64 {
    if r.product_mass <= 0.0 { 0.0 } else { r.total_input_mass / r.product_mass }
}

fn solvent_burden(r: &Route) -> f64 {
    if r.product_mass <= 0.0 { 0.0 } else { r.solvent_mass / r.product_mass }
}

fn energy_intensity(r: &Route) -> f64 {
    if r.product_mass <= 0.0 { 0.0 } else { r.energy_kwh / r.product_mass }
}

fn catalysis_score(r: &Route) -> f64 {
    if r.catalyst_loading <= 0.0 { 0.0 } else { clamp01(1.0 - r.catalyst_loading / 20.0) }
}

fn green_score(r: &Route) -> f64 {
    clamp01(
        0.15 * clamp01(atom_economy(r)) +
        0.15 * clamp01(1.0 - e_factor(r) / 25.0) +
        0.12 * clamp01(1.0 - pmi(r) / 30.0) +
        0.13 * clamp01(1.0 - r.hazard_score) +
        0.10 * clamp01(1.0 - r.solvent_hazard_score) +
        0.10 * clamp01(1.0 - energy_intensity(r) / 60.0) +
        0.08 * catalysis_score(r) +
        0.08 * r.renewable +
        0.09 * (0.5 * r.circularity + 0.5 * r.degradation)
    )
}

fn flag(r: &Route) -> &'static str {
    let s = green_score(r);
    if s >= 0.70 {
        "strong_green_design_profile"
    } else if s >= 0.50 {
        "moderate_profile_with_tradeoffs"
    } else {
        "redesign_priority"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let routes = vec![
        Route { route_name: "Route_A_Stoichiometric", chemistry_class: "small_molecule_intermediate", product_mass: 2.0, product_mw: 180.0, reactant_mw_sum: 260.0, total_input_mass: 36.0, waste_mass: 28.0, solvent_mass: 22.0, energy_kwh: 95.0, catalyst_loading: 0.0, hazard_score: 0.55, solvent_hazard_score: 0.62, renewable: 0.20, circularity: 0.30, degradation: 0.25 },
        Route { route_name: "Route_B_Catalytic", chemistry_class: "small_molecule_intermediate", product_mass: 2.4, product_mw: 180.0, reactant_mw_sum: 225.0, total_input_mass: 18.0, waste_mass: 10.0, solvent_mass: 9.0, energy_kwh: 42.0, catalyst_loading: 2.0, hazard_score: 0.30, solvent_hazard_score: 0.35, renewable: 0.55, circularity: 0.62, degradation: 0.58 },
        Route { route_name: "Route_H_Circular_Material", chemistry_class: "consumer_material", product_mass: 6.0, product_mw: 500.0, reactant_mw_sum: 610.0, total_input_mass: 38.0, waste_mass: 16.0, solvent_mass: 12.0, energy_kwh: 52.0, catalyst_loading: 1.2, hazard_score: 0.28, solvent_hazard_score: 0.30, renewable: 0.58, circularity: 0.86, degradation: 0.68 },
    ];

    let mut file = File::create("../outputs/tables/rust_green_chemistry_screening.csv")?;
    writeln!(file, "route_name,chemistry_class,atom_economy,e_factor,pmi,solvent_burden,energy_intensity,catalysis_score,green_score,flag")?;

    for route in &routes {
        writeln!(
            file,
            "{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            route.route_name,
            route.chemistry_class,
            atom_economy(route),
            e_factor(route),
            pmi(route),
            solvent_burden(route),
            energy_intensity(route),
            catalysis_score(route),
            green_score(route),
            flag(route)
        )?;
    }

    println!("Rust green chemistry screening complete.");
    Ok(())
}
