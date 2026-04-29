#[derive(Debug)]
struct WaterRecord {
    site: &'static str,
    medium: &'static str,
    analyte: &'static str,
    concentration: f64,
    unit: &'static str,
    benchmark: f64,
    flow_l_s: f64,
}

fn ratio_to_benchmark(concentration: f64, benchmark: f64) -> f64 {
    concentration / benchmark
}

fn nutrient_load_kg_day(concentration_mg_l: f64, flow_l_s: f64) -> f64 {
    concentration_mg_l * flow_l_s * 0.0864
}

fn main() {
    let records = vec![
        WaterRecord {
            site: "River-A",
            medium: "surface_water",
            analyte: "nitrate_as_N",
            concentration: 7.8,
            unit: "mg/L",
            benchmark: 10.0,
            flow_l_s: 820.0,
        },
        WaterRecord {
            site: "River-A",
            medium: "surface_water",
            analyte: "phosphate_as_P",
            concentration: 0.18,
            unit: "mg/L",
            benchmark: 0.10,
            flow_l_s: 820.0,
        },
        WaterRecord {
            site: "Urban-D",
            medium: "stormwater",
            analyte: "lead",
            concentration: 18.0,
            unit: "ug/L",
            benchmark: 15.0,
            flow_l_s: 210.0,
        },
    ];

    println!("Water chemistry screening example");
    for record in records {
        let ratio = ratio_to_benchmark(record.concentration, record.benchmark);
        let flag = if ratio > 1.0 {
            "exceeds_benchmark"
        } else {
            "below_benchmark"
        };

        println!(
            "{} | {} | {} | {:.3} {} | ratio {:.3} | {}",
            record.site,
            record.medium,
            record.analyte,
            record.concentration,
            record.unit,
            ratio,
            flag
        );

        if record.unit == "mg/L" && (record.analyte.contains("nitrate") || record.analyte.contains("phosphate")) {
            let load = nutrient_load_kg_day(record.concentration, record.flow_l_s);
            println!("  estimated load: {:.3} kg/day", load);
        }
    }
}
