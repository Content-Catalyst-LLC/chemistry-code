fn limiting_extent(available: &[f64], coefficients: &[f64]) -> f64 {
    available
        .iter()
        .zip(coefficients.iter())
        .map(|(n, coefficient)| n / coefficient)
        .fold(f64::INFINITY, f64::min)
}

fn percent_yield(actual: f64, theoretical: f64) -> f64 {
    actual / theoretical * 100.0
}

fn dilution_volume(c1: f64, c2: f64, v2: f64) -> f64 {
    (c2 * v2) / c1
}

fn main() {
    let extent = limiting_extent(&[4.0, 1.5], &[2.0, 1.0]);
    let water_mol = extent * 2.0;
    let theoretical_yield = water_mol * 18.01528;
    let yield_percent = percent_yield(45.0, theoretical_yield);
    let stock_volume = dilution_volume(1.0, 0.1, 0.25);

    println!("maximum_extent_mol={:.6}", extent);
    println!("water_mol_theoretical={:.6}", water_mol);
    println!("theoretical_yield_g={:.6}", theoretical_yield);
    println!("percent_yield={:.6}", yield_percent);
    println!("stock_volume_L={:.6}", stock_volume);
}
