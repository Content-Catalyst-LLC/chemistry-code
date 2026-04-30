#[derive(Debug)]
struct AstroRecord {
    source: &'static str,
    species: &'static str,
    rest_frequency_ghz: f64,
    observed_frequency_ghz: f64,
    column_density_cm2: f64,
    h2_column_density_cm2: f64,
}

fn radial_velocity_km_s(rest: f64, observed: f64) -> f64 {
    let c_km_s = 299_792.458_f64;
    -c_km_s * (observed - rest) / rest
}

fn fractional_abundance(column_density: f64, h2_column_density: f64) -> f64 {
    column_density / h2_column_density
}

fn main() {
    let records = vec![
        AstroRecord {
            source: "Cloud-A",
            species: "CO",
            rest_frequency_ghz: 115.271,
            observed_frequency_ghz: 115.269,
            column_density_cm2: 2.0e17,
            h2_column_density_cm2: 2.0e22,
        },
        AstroRecord {
            source: "HotCore-B",
            species: "CH3OH",
            rest_frequency_ghz: 96.741,
            observed_frequency_ghz: 96.738,
            column_density_cm2: 8.0e16,
            h2_column_density_cm2: 5.0e23,
        },
    ];

    println!("Astrochemical abundance and velocity example");

    for record in records {
        let velocity = radial_velocity_km_s(record.rest_frequency_ghz, record.observed_frequency_ghz);
        let abundance = fractional_abundance(record.column_density_cm2, record.h2_column_density_cm2);

        println!(
            "{} | {} | velocity {:.2} km/s | abundance {:.3e}",
            record.source, record.species, velocity, abundance
        );
    }
}
