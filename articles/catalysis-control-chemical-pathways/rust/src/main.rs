const R: f64 = 8.314462618;

fn rate_enhancement(delta_ea_kj_mol: f64, temperature_k: f64) -> f64 {
    ((delta_ea_kj_mol * 1000.0) / (R * temperature_k)).exp()
}

fn turnover_number(product_mol: f64, catalyst_mol: f64) -> f64 {
    product_mol / catalyst_mol
}

fn turnover_frequency(product_mol: f64, catalyst_mol: f64, time_s: f64) -> f64 {
    turnover_number(product_mol, catalyst_mol) / time_s
}

fn langmuir_theta(k: f64, p: f64) -> f64 {
    (k * p) / (1.0 + k * p)
}

fn main() {
    println!("rate_enhancement={:.6}", rate_enhancement(25.0, 298.15));
    println!("TON={:.6}", turnover_number(0.05, 0.0005));
    println!("TOF={:.8}", turnover_frequency(0.05, 0.0005, 3600.0));
    println!("theta={:.6}", langmuir_theta(1.5, 1.0));
}
