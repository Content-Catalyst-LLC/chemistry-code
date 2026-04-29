#[derive(Debug)]
struct SoilRecord {
    site: &'static str,
    land_use: &'static str,
    ph: f64,
    soc_percent: f64,
    bulk_density: f64,
    depth_cm: f64,
    phosphorus_mg_kg: f64,
    nitrate_mg_kg: f64,
    cec: f64,
    base_cations: f64,
}

fn soc_stock_mg_ha(soc_percent: f64, bulk_density: f64, depth_cm: f64) -> f64 {
    soc_percent * bulk_density * depth_cm
}

fn base_saturation_percent(base_cations: f64, cec: f64) -> f64 {
    100.0 * base_cations / cec
}

fn main() {
    let records = vec![
        SoilRecord {
            site: "Field-A",
            land_use: "row_crop",
            ph: 6.4,
            soc_percent: 1.8,
            bulk_density: 1.32,
            depth_cm: 30.0,
            phosphorus_mg_kg: 32.0,
            nitrate_mg_kg: 18.0,
            cec: 12.0,
            base_cations: 8.4,
        },
        SoilRecord {
            site: "Field-B",
            land_use: "row_crop",
            ph: 5.3,
            soc_percent: 1.1,
            bulk_density: 1.45,
            depth_cm: 30.0,
            phosphorus_mg_kg: 68.0,
            nitrate_mg_kg: 42.0,
            cec: 8.5,
            base_cations: 4.2,
        },
    ];

    println!("Soil chemistry screening example");

    for record in records {
        let soc_stock = soc_stock_mg_ha(record.soc_percent, record.bulk_density, record.depth_cm);
        let base_sat = base_saturation_percent(record.base_cations, record.cec);
        let ph_flag = if record.ph < 5.8 { "acidic_screen" } else { "not_acidic_screen" };
        let p_flag = if record.phosphorus_mg_kg > 60.0 { "high_P_attention" } else { "not_high_P" };
        let n_flag = if record.nitrate_mg_kg > 30.0 { "high_nitrate_attention" } else { "not_high_nitrate" };

        println!(
            "{} | {} | pH {:.2} {} | SOC stock {:.2} Mg/ha | base saturation {:.1}% | {} | {}",
            record.site, record.land_use, record.ph, ph_flag, soc_stock, base_sat, p_flag, n_flag
        );
    }
}
