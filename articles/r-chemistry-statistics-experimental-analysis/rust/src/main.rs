fn mean(values: &[f64]) -> f64 {
    values.iter().sum::<f64>() / values.len() as f64
}

fn sample_sd(values: &[f64]) -> f64 {
    let xbar = mean(values);
    let variance = values.iter().map(|x| (x - xbar).powi(2)).sum::<f64>() / (values.len() as f64 - 1.0);
    variance.sqrt()
}

fn standard_error(values: &[f64]) -> f64 {
    sample_sd(values) / (values.len() as f64).sqrt()
}

fn rsd_percent(values: &[f64]) -> f64 {
    100.0 * sample_sd(values) / mean(values)
}

fn unknown_concentration(response: f64, slope: f64, intercept: f64) -> f64 {
    (response - intercept) / slope
}

fn main() {
    let values = [1.02, 1.05, 0.99];

    println!("mean={:.6}", mean(&values));
    println!("sample_sd={:.6}", sample_sd(&values));
    println!("standard_error={:.6}", standard_error(&values));
    println!("rsd_percent={:.6}", rsd_percent(&values));
    println!("unknown_concentration={:.6}", unknown_concentration(0.95, 0.30, 0.02));
}
