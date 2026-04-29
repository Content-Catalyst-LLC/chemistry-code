fn boltzmann_weight(delta_e_kj_mol: f64, temperature_k: f64) -> f64 {
    let r = 8.314462618;
    (-(delta_e_kj_mol * 1000.0) / (r * temperature_k)).exp()
}

fn lennard_jones(distance: f64, epsilon: f64, sigma: f64) -> f64 {
    let ratio = sigma / distance;
    4.0 * epsilon * (ratio.powi(12) - ratio.powi(6))
}

fn tanimoto(a: f64, b: f64, c: f64) -> f64 {
    c / (a + b - c)
}

fn main() {
    println!("boltzmann_weight={:.6}", boltzmann_weight(2.5, 298.15));
    println!("lennard_jones={:.6}", lennard_jones(1.12, 1.0, 1.0));
    println!("tanimoto={:.6}", tanimoto(5.0, 4.0, 3.0));
}
