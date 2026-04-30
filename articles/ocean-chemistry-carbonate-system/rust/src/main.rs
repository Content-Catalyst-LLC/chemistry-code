#[derive(Debug)]
struct OceanSample {
    station: &'static str,
    ph: f64,
    dic_umol_kg: f64,
    calcium_mmol_kg: f64,
    pco2_uatm: f64,
}

fn carbonate_alpha2(ph: f64) -> f64 {
    let k1 = 10.0_f64.powf(-6.0);
    let k2 = 10.0_f64.powf(-9.1);
    let h = 10.0_f64.powf(-ph);
    let denominator = h.powi(2) + k1 * h + k1 * k2;
    k1 * k2 / denominator
}

fn omega_aragonite(calcium_mmol_kg: f64, carbonate_umol_kg: f64) -> f64 {
    let ksp_aragonite = 6.5e-7;
    (calcium_mmol_kg * 1.0e-3) * (carbonate_umol_kg * 1.0e-6) / ksp_aragonite
}

fn main() {
    let samples = vec![
        OceanSample {
            station: "Open-Ocean-A",
            ph: 8.10,
            dic_umol_kg: 2050.0,
            calcium_mmol_kg: 10.3,
            pco2_uatm: 410.0,
        },
        OceanSample {
            station: "Upwelling-B",
            ph: 7.78,
            dic_umol_kg: 2240.0,
            calcium_mmol_kg: 10.1,
            pco2_uatm: 820.0,
        },
    ];

    println!("Ocean carbonate screening example");

    for sample in samples {
        let alpha2 = carbonate_alpha2(sample.ph);
        let carbonate = alpha2 * sample.dic_umol_kg;
        let omega = omega_aragonite(sample.calcium_mmol_kg, carbonate);
        let flux_proxy = sample.pco2_uatm - 420.0;
        let flag = if omega < 2.0 {
            "low_aragonite_saturation_attention"
        } else {
            "higher_aragonite_saturation_screen"
        };

        println!(
            "{} | pH {:.2} | carbonate {:.2} umol/kg | Omega_arag {:.2} | CO2 flux proxy {:.1} uatm | {}",
            sample.station, sample.ph, carbonate, omega, flux_proxy, flag
        );
    }
}
