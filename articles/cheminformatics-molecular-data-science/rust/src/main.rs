fn tanimoto(a: f64, b: f64, c: f64) -> f64 {
    c / (a + b - c)
}

fn pic50(ic50_nm: f64) -> f64 {
    let ic50_m = ic50_nm * 1.0e-9;
    -ic50_m.log10()
}

fn euclidean_distance(x: &[f64], y: &[f64]) -> f64 {
    x.iter()
        .zip(y.iter())
        .map(|(xi, yi)| (xi - yi).powi(2))
        .sum::<f64>()
        .sqrt()
}

fn main() {
    println!("tanimoto={:.6}", tanimoto(5.0, 4.0, 3.0));
    println!("pIC50={:.6}", pic50(50.0));
    println!("distance={:.6}", euclidean_distance(&[1.0, 2.0, 3.0], &[1.5, 2.5, 4.0]));
}
