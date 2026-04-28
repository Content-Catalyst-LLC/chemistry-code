fn weak_acid_hydronium(ka: f64, concentration: f64) -> f64 {
    (-ka + (ka.powi(2) + 4.0 * ka * concentration).sqrt()) / 2.0
}

fn ph_from_hydronium(h: f64) -> f64 {
    -h.log10()
}

fn henderson_hasselbalch(pka: f64, base: f64, acid: f64) -> f64 {
    pka + (base / acid).log10()
}

fn main() {
    let h = weak_acid_hydronium(1.8e-5, 0.100);
    let ph = ph_from_hydronium(h);
    let buffer_ph = henderson_hasselbalch(4.76, 0.120, 0.100);

    println!("weak_acid_hydronium={:.8}", h);
    println!("weak_acid_pH={:.6}", ph);
    println!("buffer_pH={:.6}", buffer_ph);
}
