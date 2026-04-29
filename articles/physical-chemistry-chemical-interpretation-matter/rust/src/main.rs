const R: f64 = 8.314462618;
const F: f64 = 96485.33212;

fn equilibrium_constant(delta_g_kj_mol: f64, temperature_k: f64) -> f64 {
    (-(delta_g_kj_mol * 1000.0) / (R * temperature_k)).exp()
}

fn arrhenius(a: f64, ea_kj_mol: f64, temperature_k: f64) -> f64 {
    a * (-(ea_kj_mol * 1000.0) / (R * temperature_k)).exp()
}

fn nernst(e0: f64, n: f64, q: f64, temperature_k: f64) -> f64 {
    e0 - (R * temperature_k / (n * F)) * q.ln()
}

fn main() {
    println!("K_demo={:.6}", equilibrium_constant(-20.0, 298.15));
    println!("k_demo={:.6e}", arrhenius(1.0e12, 75.0, 298.15));
    println!("E_demo={:.6}", nernst(1.10, 2.0, 100.0, 298.15));
}
