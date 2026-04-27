// Safe introductory Chemical Revolution calculator.

fn oxide_mass(metal_mass_g: f64, oxygen_mass_g: f64) -> f64 {
    metal_mass_g + oxygen_mass_g
}

fn oxygen_mass_fraction(metal_mass_g: f64, oxygen_mass_g: f64) -> f64 {
    oxygen_mass_g / oxide_mass(metal_mass_g, oxygen_mass_g)
}

fn mass_difference(reactant_mass_g: f64, product_mass_g: f64) -> f64 {
    product_mass_g - reactant_mass_g
}

fn main() {
    let oxide = oxide_mass(24.305, 16.000);
    let fraction = oxygen_mass_fraction(24.305, 16.000);
    let diff = mass_difference(44.0, 44.0);

    println!("magnesium_oxide_mass_g={:.5}", oxide);
    println!("oxygen_mass_fraction={:.5}", fraction);
    println!("mass_difference_closed_system={:.5}", diff);
}
