// Safe introductory chemical metrology calculator.

fn combined_standard_uncertainty(components: &[f64]) -> f64 {
    components.iter().map(|x| x * x).sum::<f64>().sqrt()
}

fn expanded_uncertainty(uc: f64, k: f64) -> f64 {
    k * uc
}

fn normalized_error(x_lab: f64, x_ref: f64, u_lab: f64, u_ref: f64) -> f64 {
    (x_lab - x_ref) / (u_lab.powi(2) + u_ref.powi(2)).sqrt()
}

fn main() {
    let components = [0.004, 0.006, 0.010, 0.015, 0.012, 0.020];
    let uc = combined_standard_uncertainty(&components);
    let expanded = expanded_uncertainty(uc, 2.0);
    let en = normalized_error(10.2, 10.0, 0.8, 0.4);

    println!("combined_standard_uncertainty={:.6}", uc);
    println!("expanded_uncertainty={:.6}", expanded);
    println!("normalized_error={:.6}", en);
}
