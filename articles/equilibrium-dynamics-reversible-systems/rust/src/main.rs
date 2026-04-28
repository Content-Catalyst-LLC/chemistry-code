const R: f64 = 8.314462618;

fn delta_g_from_qk(q: f64, k: f64, temperature_k: f64) -> f64 {
    R * temperature_k * (q / k).ln() / 1000.0
}

fn solve_isomerization(k: f64, total: f64) -> (f64, f64) {
    let a_eq = total / (1.0 + k);
    let b_eq = total - a_eq;
    (a_eq, b_eq)
}

fn reversible_step(a: f64, b: f64, kf: f64, kr: f64, dt: f64) -> (f64, f64) {
    let net = kf * a - kr * b;
    ((a - net * dt).max(0.0), (b + net * dt).max(0.0))
}

fn main() {
    let (a_eq, b_eq) = solve_isomerization(4.0, 1.0);
    let dg = delta_g_from_qk(0.5, 4.0, 298.15);
    let (a1, b1) = reversible_step(1.0, 0.0, 0.20, 0.05, 0.25);

    println!("A_eq={:.6}", a_eq);
    println!("B_eq={:.6}", b_eq);
    println!("delta_g_kj_mol={:.6}", dg);
    println!("A_after_step={:.6}", a1);
    println!("B_after_step={:.6}", b1);
}
