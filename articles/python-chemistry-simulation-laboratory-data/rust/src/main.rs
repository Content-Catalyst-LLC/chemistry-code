fn unknown_concentration(response: f64, slope: f64, intercept: f64) -> f64 {
    (response - intercept) / slope
}

fn first_order_concentration(c0: f64, k: f64, t: f64) -> f64 {
    c0 * (-k * t).exp()
}

fn half_life_first_order(k: f64) -> f64 {
    2.0_f64.ln() / k
}

fn standard_error(sd: f64, n: f64) -> f64 {
    sd / n.sqrt()
}

fn main() {
    println!("unknown_concentration_mM={:.6}", unknown_concentration(0.95, 0.30, 0.02));
    println!("first_order_concentration_mM={:.6}", first_order_concentration(10.0, 0.015, 100.0));
    println!("half_life_s={:.6}", half_life_first_order(0.015));
    println!("standard_error={:.6}", standard_error(0.03, 3.0));
}
