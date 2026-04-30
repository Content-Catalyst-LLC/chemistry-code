#[derive(Debug)]
struct RockSample {
    sample_id: &'static str,
    rock_type: &'static str,
    al2o3: f64,
    cao: f64,
    na2o: f64,
    k2o: f64,
    rb_ppm: f64,
    sr_ppm: f64,
}

fn cia_simplified(al2o3: f64, cao: f64, na2o: f64, k2o: f64) -> f64 {
    100.0 * al2o3 / (al2o3 + cao + na2o + k2o)
}

fn ratio(numerator: f64, denominator: f64) -> f64 {
    numerator / denominator
}

fn radiometric_age_ma(parent: f64, daughter: f64, lambda: f64) -> f64 {
    (1.0 / lambda) * (1.0 + daughter / parent).ln() / 1.0e6
}

fn main() {
    let samples = vec![
        RockSample {
            sample_id: "GEO001",
            rock_type: "basalt",
            al2o3: 15.4,
            cao: 10.5,
            na2o: 2.9,
            k2o: 0.8,
            rb_ppm: 12.0,
            sr_ppm: 420.0,
        },
        RockSample {
            sample_id: "GEO004",
            rock_type: "weathered_saprolite",
            al2o3: 25.5,
            cao: 0.8,
            na2o: 0.3,
            k2o: 1.2,
            rb_ppm: 45.0,
            sr_ppm: 85.0,
        },
    ];

    println!("Geochemical index examples");

    for sample in samples {
        let cia = cia_simplified(sample.al2o3, sample.cao, sample.na2o, sample.k2o);
        let rb_sr = ratio(sample.rb_ppm, sample.sr_ppm);
        println!(
            "{} | {} | CIA {:.2} | Rb/Sr {:.3}",
            sample.sample_id, sample.rock_type, cia, rb_sr
        );
    }

    let age = radiometric_age_ma(1.0, 0.35, 1.55125e-10);
    println!("Simplified radiometric age: {:.2} Ma", age);
}
