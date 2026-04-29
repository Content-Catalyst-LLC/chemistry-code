#[derive(Debug)]
struct AtmosphericRecord {
    site: &'static str,
    analyte: &'static str,
    class_name: &'static str,
    concentration: f64,
    unit: &'static str,
    reference_value: f64,
}

fn ratio_to_reference(concentration: f64, reference_value: f64) -> f64 {
    concentration / reference_value
}

fn co2_forcing(current_ppm: f64, reference_ppm: f64) -> f64 {
    5.35 * (current_ppm / reference_ppm).ln()
}

fn first_order_concentration(c0: f64, k_per_day: f64, t_days: f64) -> f64 {
    c0 * (-k_per_day * t_days).exp()
}

fn main() {
    let records = vec![
        AtmosphericRecord {
            site: "Background-A",
            analyte: "CO2",
            class_name: "long_lived_greenhouse_gas",
            concentration: 423.0,
            unit: "ppm",
            reference_value: 280.0,
        },
        AtmosphericRecord {
            site: "Urban-B",
            analyte: "O3",
            class_name: "secondary_pollutant",
            concentration: 0.074,
            unit: "ppm",
            reference_value: 0.070,
        },
        AtmosphericRecord {
            site: "Urban-B",
            analyte: "PM2.5",
            class_name: "aerosol_particle",
            concentration: 17.2,
            unit: "ug/m3",
            reference_value: 15.0,
        },
    ];

    println!("Atmospheric chemistry screening example");
    for record in records {
        let ratio = ratio_to_reference(record.concentration, record.reference_value);
        let flag = if ratio > 1.0 {
            "above_reference"
        } else {
            "at_or_below_reference"
        };

        println!(
            "{} | {} | {} | {:.4} {} | ratio {:.3} | {}",
            record.site,
            record.analyte,
            record.class_name,
            record.concentration,
            record.unit,
            ratio,
            flag
        );
    }

    let forcing = co2_forcing(423.0, 280.0);
    println!("\nApproximate CO2 forcing: {:.3} W/m2", forcing);

    println!("\nFirst-order atmospheric decay example");
    for day in (0..=30).step_by(5) {
        let c = first_order_concentration(100.0, 0.20, day as f64);
        println!("day {:>2}: {:.3} ppb", day, c);
    }
}
