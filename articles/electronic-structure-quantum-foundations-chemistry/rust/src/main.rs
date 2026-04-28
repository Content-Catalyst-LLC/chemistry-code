const H: f64 = 6.626_070_15e-34;
const C: f64 = 299_792_458.0;
const EV_TO_J: f64 = 1.602_176_634e-19;
const ELECTRON_MASS: f64 = 9.109_383_7139e-31;

fn hydrogen_energy_ev(n: f64) -> f64 {
    -13.6 / (n * n)
}

fn photon_wavelength_nm(delta_energy_ev: f64) -> f64 {
    let delta_j = delta_energy_ev * EV_TO_J;
    (H * C / delta_j) * 1.0e9
}

fn particle_in_box_energy_ev(n: f64, box_length_nm: f64) -> f64 {
    let length_m = box_length_nm * 1.0e-9;
    let energy_j = (n * n * H * H) / (8.0 * ELECTRON_MASS * length_m * length_m);
    energy_j / EV_TO_J
}

fn main() {
    let e1 = hydrogen_energy_ev(1.0);
    let e2 = hydrogen_energy_ev(2.0);
    let wavelength = photon_wavelength_nm((e2 - e1).abs());
    let box_e1 = particle_in_box_energy_ev(1.0, 1.0);

    println!("hydrogen_n1_energy_eV={:.6}", e1);
    println!("hydrogen_n2_energy_eV={:.6}", e2);
    println!("n2_to_n1_wavelength_nm={:.3}", wavelength);
    println!("particle_box_n1_1nm_eV={:.6}", box_e1);
}
