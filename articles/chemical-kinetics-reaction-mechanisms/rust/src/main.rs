const R: f64 = 8.314462618;

fn first_order_concentration(c0: f64, k: f64, t: f64) -> f64 {
    c0 * (-k * t).exp()
}

fn half_life_first_order(k: f64) -> f64 {
    std::f64::consts::LN_2 / k
}

fn arrhenius_rate_constant(a: f64, ea_j_mol: f64, temperature_k: f64) -> f64 {
    a * (-(ea_j_mol) / (R * temperature_k)).exp()
}

fn main() {
    println!("first_order_concentration_t20={:.6}", first_order_concentration(1.0, 0.15, 20.0));
    println!("first_order_half_life={:.6}", half_life_first_order(0.15));
    println!("arrhenius_k_310K={:.6}", arrhenius_rate_constant(1.0e7, 55000.0, 310.0));
}
