// Safe introductory mathematical chemistry calculator.

fn first_order_concentration(initial: f64, rate_constant: f64, time: f64) -> f64 {
    initial * (-rate_constant * time).exp()
}

fn equilibrium_constant(delta_g_standard_kj_mol: f64, temperature_k: f64) -> f64 {
    let r = 8.314_462_618_f64;
    (-(delta_g_standard_kj_mol * 1000.0) / (r * temperature_k)).exp()
}

fn distance(a: [f64; 3], b: [f64; 3]) -> f64 {
    ((a[0] - b[0]).powi(2) + (a[1] - b[1]).powi(2) + (a[2] - b[2]).powi(2)).sqrt()
}

fn main() {
    let concentration = first_order_concentration(1.0, 0.15, 10.0);
    let k_eq = equilibrium_constant(-5.0, 298.15);
    let d_oh = distance([0.0, 0.0, 0.0], [0.958, 0.0, 0.0]);

    println!("first_order_concentration_t10={:.6}", concentration);
    println!("equilibrium_constant={:.6}", k_eq);
    println!("distance_oh_angstrom={:.6}", d_oh);
}
