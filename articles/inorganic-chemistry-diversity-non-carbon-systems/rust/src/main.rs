fn oxidation_state(total_charge: f64, known_contribution: f64, unknown_atom_count: f64) -> f64 {
    (total_charge - known_contribution) / unknown_atom_count
}

fn cfse(t2g_electrons: f64, eg_electrons: f64, delta_o: f64) -> f64 {
    t2g_electrons * (-0.4 * delta_o) + eg_electrons * (0.6 * delta_o)
}

fn spin_only_moment(unpaired_electrons: f64) -> f64 {
    (unpaired_electrons * (unpaired_electrons + 2.0)).sqrt()
}

fn tolerance_factor(r_a: f64, r_b: f64, r_x: f64) -> f64 {
    (r_a + r_x) / (2.0_f64.sqrt() * (r_b + r_x))
}

fn main() {
    println!("Mn_in_KMnO4_OS={:.6}", oxidation_state(0.0, -7.0, 1.0));
    println!("octahedral_d3_CFSE={:.6}", cfse(3.0, 0.0, 1.0));
    println!("spin_only_d3={:.6}", spin_only_moment(3.0));
    println!("tolerance_factor={:.6}", tolerance_factor(1.60, 0.60, 1.40));
}
