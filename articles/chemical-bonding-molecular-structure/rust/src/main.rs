fn bond_order(bonding_electrons: f64, antibonding_electrons: f64) -> f64 {
    (bonding_electrons - antibonding_electrons) / 2.0
}

fn electronegativity_difference(chi_a: f64, chi_b: f64) -> f64 {
    (chi_a - chi_b).abs()
}

fn distance(a: [f64; 3], b: [f64; 3]) -> f64 {
    let dx = a[0] - b[0];
    let dy = a[1] - b[1];
    let dz = a[2] - b[2];
    (dx * dx + dy * dy + dz * dz).sqrt()
}

fn main() {
    let oh_distance = distance([0.0, 0.0, 0.0], [0.958, 0.0, 0.0]);
    let oh_delta_chi = electronegativity_difference(3.44, 2.20);
    let h2_bond_order = bond_order(2.0, 0.0);

    println!("oh_distance_angstrom={:.6}", oh_distance);
    println!("oh_delta_chi={:.6}", oh_delta_chi);
    println!("h2_bond_order={:.6}", h2_bond_order);
}
