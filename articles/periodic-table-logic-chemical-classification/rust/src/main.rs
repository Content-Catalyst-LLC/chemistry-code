fn isotope_weighted_mass(masses: &[f64], abundances: &[f64]) -> f64 {
    masses
        .iter()
        .zip(abundances.iter())
        .map(|(mass, abundance)| mass * abundance)
        .sum()
}

fn neutron_number(mass_number: i32, atomic_number: i32) -> i32 {
    mass_number - atomic_number
}

fn feature_distance(a: &[f64], b: &[f64]) -> f64 {
    a.iter()
        .zip(b.iter())
        .map(|(x, y)| (x - y).powi(2))
        .sum::<f64>()
        .sqrt()
}

fn main() {
    let chlorine_mass = isotope_weighted_mass(
        &[34.96885268, 36.96590260],
        &[0.7576, 0.2424],
    );

    let c13_neutrons = neutron_number(13, 6);
    let li_na_distance = feature_distance(
        &[1.0, 2.0, 128.0, 520.0],
        &[1.0, 3.0, 166.0, 496.0],
    );

    println!("chlorine_weighted_atomic_mass_u={:.6}", chlorine_mass);
    println!("carbon_13_neutron_number={}", c13_neutrons);
    println!("li_na_feature_distance_unscaled={:.6}", li_na_distance);
}
