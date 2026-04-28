const R: f64 = 8.314462618;

fn gibbs_free_energy(delta_h_kj_mol: f64, delta_s_j_mol_k: f64, temperature_k: f64) -> f64 {
    delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0
}

fn equilibrium_constant(delta_g_standard_kj_mol: f64, temperature_k: f64) -> f64 {
    (-(delta_g_standard_kj_mol * 1000.0) / (R * temperature_k)).exp()
}

fn calorimetry_delta_h(mass_g: f64, specific_heat_j_g_k: f64, delta_t_k: f64, amount_mol: f64) -> f64 {
    let q_solution_j = mass_g * specific_heat_j_g_k * delta_t_k;
    let q_reaction_j = -q_solution_j;
    q_reaction_j / 1000.0 / amount_mol
}

fn main() {
    let dg = gibbs_free_energy(-80.0, -100.0, 298.15);
    let k = equilibrium_constant(dg, 298.15);
    let dh_cal = calorimetry_delta_h(100.0, 4.184, 6.2, 0.0500);

    println!("delta_g_kj_mol={:.6}", dg);
    println!("equilibrium_constant={:.6}", k);
    println!("calorimetry_delta_h_kj_mol={:.6}", dh_cal);
}
