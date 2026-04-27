// Safe introductory chemistry calculator.

fn moles_from_mass(mass_g: f64, molar_mass_g_mol: f64) -> f64 {
    mass_g / molar_mass_g_mol
}

fn molarity(moles: f64, volume_l: f64) -> f64 {
    moles / volume_l
}

fn first_order_concentration(initial: f64, rate_constant: f64, time: f64) -> f64 {
    initial * (-rate_constant * time).exp()
}

fn main() {
    let moles = moles_from_mass(5.844, 58.44);
    let concentration = molarity(moles, 0.500);
    let remaining = first_order_concentration(1.0, 0.15, 10.0);

    println!("moles={:.5}", moles);
    println!("molarity_mol_l={:.5}", concentration);
    println!("first_order_concentration={:.5}", remaining);
}
