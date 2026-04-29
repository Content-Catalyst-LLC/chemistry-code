#[derive(Debug)]
struct MonitoringRecord {
    site: &'static str,
    medium: &'static str,
    analyte: &'static str,
    concentration: f64,
    benchmark: f64,
    unit: &'static str,
}

fn hazard_quotient(concentration: f64, benchmark: f64) -> f64 {
    concentration / benchmark
}

fn first_order_concentration(c0: f64, k: f64, t_days: f64) -> f64 {
    c0 * (-k * t_days).exp()
}

fn main() {
    let records = vec![
        MonitoringRecord {
            site: "River-A",
            medium: "surface_water",
            analyte: "nitrate_as_N",
            concentration: 7.8,
            benchmark: 10.0,
            unit: "mg/L",
        },
        MonitoringRecord {
            site: "Urban-C",
            medium: "air",
            analyte: "PM2.5",
            concentration: 18.5,
            benchmark: 15.0,
            unit: "ug/m3",
        },
        MonitoringRecord {
            site: "Industrial-E",
            medium: "groundwater",
            analyte: "benzene",
            concentration: 6.2,
            benchmark: 5.0,
            unit: "ug/L",
        },
    ];

    println!("Environmental chemistry screening example");
    for record in records {
        let hq = hazard_quotient(record.concentration, record.benchmark);
        let flag = if hq > 1.0 {
            "exceeds_benchmark"
        } else {
            "below_benchmark"
        };

        println!(
            "{} | {} | {} | {:.3} {} | HQ {:.3} | {}",
            record.site, record.medium, record.analyte, record.concentration, record.unit, hq, flag
        );
    }

    let c0 = 100.0;
    let k = 0.08;
    let half_life = std::f64::consts::LN_2 / k;

    println!("\nFirst-order persistence");
    println!("Half-life: {:.2} days", half_life);

    for day in (0..=60).step_by(10) {
        let c = first_order_concentration(c0, k, day as f64);
        println!("day {:>2}: {:.3} ug/L", day, c);
    }
}
