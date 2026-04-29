fn concentration_from_calibration(signal: f64, slope: f64, intercept: f64) -> f64 {
    (signal - intercept) / slope
}

fn lod(blank_sd: f64, slope: f64) -> f64 {
    3.0 * blank_sd / slope
}

fn loq(blank_sd: f64, slope: f64) -> f64 {
    10.0 * blank_sd / slope
}

fn chromatographic_resolution(tr1: f64, tr2: f64, w1: f64, w2: f64) -> f64 {
    2.0 * (tr2 - tr1) / (w1 + w2)
}

fn beer_lambert_concentration(absorbance: f64, epsilon: f64, path_length: f64) -> f64 {
    absorbance / (epsilon * path_length)
}

fn main() {
    println!("unknown_concentration={:.6}", concentration_from_calibration(3.72, 0.515, 0.04));
    println!("LOD={:.6}", lod(0.0032, 0.515));
    println!("LOQ={:.6}", loq(0.0032, 0.515));
    println!("resolution={:.6}", chromatographic_resolution(3.10, 5.20, 0.42, 0.50));
    println!("beer_lambert_c={:.8}", beer_lambert_concentration(0.625, 12500.0, 1.0));
}
