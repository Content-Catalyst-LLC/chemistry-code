const AVOGADRO_CONSTANT: f64 = 6.022_140_76e23;

fn neutron_number(mass_number: i32, atomic_number: i32) -> i32 {
    mass_number - atomic_number
}

fn isotope_weighted_mass(masses: &[f64], abundances: &[f64]) -> f64 {
    masses
        .iter()
        .zip(abundances.iter())
        .map(|(mass, abundance)| mass * abundance)
        .sum()
}

fn amount_from_mass(mass_g: f64, molar_mass_g_mol: f64) -> f64 {
    mass_g / molar_mass_g_mol
}

fn main() {
    let chlorine_mass = isotope_weighted_mass(
        &[34.96885268, 36.96590260],
        &[0.7576, 0.2424],
    );
    let carbon_14_neutrons = neutron_number(14, 6);
    let water_moles = amount_from_mass(18.015, 18.015);
    let entities = water_moles * AVOGADRO_CONSTANT;

    println!("chlorine_weighted_atomic_mass_u={:.6}", chlorine_mass);
    println!("carbon_14_neutron_number={}", carbon_14_neutrons);
    println!("water_amount_mol={:.6}", water_moles);
    println!("water_estimated_entities={:.6e}", entities);
}
