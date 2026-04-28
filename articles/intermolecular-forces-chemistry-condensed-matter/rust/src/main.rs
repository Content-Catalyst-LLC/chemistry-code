fn lennard_jones(r_angstrom: f64, epsilon_kj_mol: f64, sigma_angstrom: f64) -> f64 {
    let ratio = sigma_angstrom / r_angstrom;
    4.0 * epsilon_kj_mol * (ratio.powi(12) - ratio.powi(6))
}

fn coulomb_relative(q1: f64, q2: f64, r: f64) -> f64 {
    q1 * q2 / r
}

fn main() {
    let epsilon = 0.997_f64;
    let sigma = 3.40_f64;
    let r_min = 2.0_f64.powf(1.0 / 6.0) * sigma;
    let u_min = lennard_jones(r_min, epsilon, sigma);

    println!("r_min_angstrom={:.6}", r_min);
    println!("u_min_kj_mol={:.6}", u_min);
    println!("relative_coulomb_attraction={:.6}", coulomb_relative(1.0, -1.0, 2.0));
}
