fn boltzmann_weight(delta_e_kj_mol: f64, temperature_k: f64) -> f64 {
    let r = 8.314462618;
    (-(delta_e_kj_mol * 1000.0) / (r * temperature_k)).exp()
}

fn tst_rate(delta_g_dagger_kj_mol: f64, temperature_k: f64) -> f64 {
    let kb = 1.380649e-23;
    let h = 6.62607015e-34;
    let r = 8.314462618;
    (kb * temperature_k / h) * (-(delta_g_dagger_kj_mol * 1000.0) / (r * temperature_k)).exp()
}

fn two_level_energies(ea: f64, eb: f64, v: f64) -> (f64, f64) {
    let trace = ea + eb;
    let diff = ea - eb;
    let split = (diff.powi(2) + 4.0 * v.powi(2)).sqrt();
    ((trace - split) / 2.0, (trace + split) / 2.0)
}

fn main() {
    let (e1, e2) = two_level_energies(-10.0, -8.0, -2.0);
    println!("two_level_E1={:.6}", e1);
    println!("two_level_E2={:.6}", e2);
    println!("boltzmann_weight={:.10}", boltzmann_weight(25.0, 298.15));
    println!("tst_rate={:.6e}", tst_rate(50.0, 298.15));
}
