const R: f64 = 8.314462618;
const F: f64 = 96485.33212;

fn cell_potential(e_cathode: f64, e_anode: f64) -> f64 {
    e_cathode - e_anode
}

fn delta_g(n: f64, e_cell: f64) -> f64 {
    -n * F * e_cell / 1000.0
}

fn nernst(e0: f64, n: f64, q: f64, temperature_k: f64) -> f64 {
    e0 - (R * temperature_k / (n * F)) * q.ln()
}

fn main() {
    let e_cell = cell_potential(0.34, -0.76);
    let dg = delta_g(2.0, e_cell);
    let e_nonstandard = nernst(1.10, 2.0, 100.0, 298.15);

    println!("E_cell_standard_V={:.6}", e_cell);
    println!("delta_g_standard_kj_mol={:.6}", dg);
    println!("E_nonstandard_V={:.6}", e_nonstandard);
}
