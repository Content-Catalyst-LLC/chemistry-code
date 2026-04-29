fn dose_response(concentration: f64, ec50: f64, hill: f64, bottom: f64, top: f64) -> f64 {
    bottom + (top - bottom) / (1.0 + (ec50 / concentration).powf(hill))
}

fn occupancy(ligand: f64, kd: f64) -> f64 {
    ligand / (kd + ligand)
}

fn target_engagement(signal_control: f64, signal_treated: f64, signal_max: f64) -> f64 {
    (signal_control - signal_treated) / (signal_control - signal_max)
}

fn main() {
    println!("response={:.6}", dose_response(1.0, 1.5, 1.2, 0.05, 1.0));
    println!("occupancy={:.6}", occupancy(2.0, 2.0));
    println!("target_engagement={:.6}", target_engagement(100.0, 55.0, 20.0));
}
