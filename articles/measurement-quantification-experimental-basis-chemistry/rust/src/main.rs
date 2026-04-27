// Safe introductory measurement and quantification calculator.

fn moles_from_mass(mass_g: f64, molar_mass_g_mol: f64) -> f64 {
    mass_g / molar_mass_g_mol
}

fn concentration_mol_l(moles: f64, volume_l: f64) -> f64 {
    moles / volume_l
}

fn dilution_stock_volume(c1: f64, c2: f64, v2: f64) -> f64 {
    (c2 * v2) / c1
}

fn expanded_uncertainty(standard_uncertainty: f64, coverage_factor: f64) -> f64 {
    standard_uncertainty * coverage_factor
}

fn main() {
    let moles = moles_from_mass(5.844, 58.44);
    let concentration = concentration_mol_l(moles, 0.500);
    let stock_volume = dilution_stock_volume(1.0, 0.10, 100.0);
    let uncertainty = expanded_uncertainty(0.0001, 2.0);

    println!("moles={:.6}", moles);
    println!("concentration_mol_l={:.6}", concentration);
    println!("stock_volume_ml={:.6}", stock_volume);
    println!("expanded_uncertainty={:.6}", uncertainty);
}
