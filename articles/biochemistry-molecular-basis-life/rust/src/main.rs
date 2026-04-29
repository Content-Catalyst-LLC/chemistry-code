fn michaelis_menten(substrate: f64, vmax: f64, km: f64) -> f64 {
    vmax * substrate / (km + substrate)
}

fn occupancy(ligand: f64, kd: f64) -> f64 {
    ligand / (kd + ligand)
}

fn hill_occupancy(ligand: f64, kd: f64, n: f64) -> f64 {
    ligand.powf(n) / (kd.powf(n) + ligand.powf(n))
}

fn delta_g_standard(k: f64, temperature_k: f64) -> f64 {
    let r = 8.314462618;
    -(r * temperature_k * k.ln()) / 1000.0
}

fn main() {
    println!("velocity={:.6}", michaelis_menten(5.0, 120.0, 3.5));
    println!("occupancy={:.6}", occupancy(2.0, 2.0));
    println!("hill_occupancy={:.6}", hill_occupancy(2.0, 2.0, 2.0));
    println!("delta_g_kj_mol={:.6}", delta_g_standard(1000.0, 298.15));
}
