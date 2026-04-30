// Medicinal Chemistry and Drug Discovery
// Rust candidate scoring and decision logic.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Candidate {
    compound_id: &'static str,
    ic50_nm: f64,
    off_target_ic50_nm: f64,
    clogp: f64,
    solubility_um: f64,
    permeability: f64,
    herg_ic50_um: f64,
    cyp_ic50_um: f64,
    assay_qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn pic50(ic50_nm: f64) -> f64 {
    -(ic50_nm * 1e-9).log10()
}

fn lle(candidate: &Candidate) -> f64 {
    pic50(candidate.ic50_nm) - candidate.clogp
}

fn selectivity(candidate: &Candidate) -> f64 {
    if candidate.ic50_nm <= 0.0 {
        0.0
    } else {
        candidate.off_target_ic50_nm / candidate.ic50_nm
    }
}

fn liability(candidate: &Candidate) -> f64 {
    let herg = clamp01((10.0 - candidate.herg_ic50_um) / 10.0);
    let cyp = clamp01((20.0 - candidate.cyp_ic50_um) / 20.0);
    clamp01(0.60 * herg + 0.40 * cyp)
}

fn mpo(candidate: &Candidate) -> f64 {
    let potency = clamp01((pic50(candidate.ic50_nm) - 5.0) / 3.0);
    let selectivity_score = clamp01(selectivity(candidate).max(1.0).log10() / 3.0);
    let lle_score = clamp01((lle(candidate) - 2.0) / 5.0);
    let solubility = clamp01(candidate.solubility_um.max(0.001).log10() / 2.3);
    let permeability = clamp01(candidate.permeability / 30.0);
    let safety = 1.0 - liability(candidate);

    clamp01(
        0.24 * potency +
        0.18 * selectivity_score +
        0.18 * lle_score +
        0.14 * solubility +
        0.14 * permeability +
        0.08 * safety +
        0.04 * candidate.assay_qc
    )
}

fn recommendation(candidate: &Candidate) -> &'static str {
    let score = mpo(candidate);
    let risk = liability(candidate);

    if risk >= 0.60 {
        "redesign_liability"
    } else if score >= 0.72 {
        "advance_to_integrated_profiling"
    } else if score >= 0.55 {
        "optimize"
    } else {
        "hold_or_redesign"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let candidates = vec![
        Candidate { compound_id: "MEDADV001", ic50_nm: 18.0, off_target_ic50_nm: 2100.0, clogp: 3.2, solubility_um: 45.0, permeability: 18.0, herg_ic50_um: 18.0, cyp_ic50_um: 22.0, assay_qc: 0.94 },
        Candidate { compound_id: "MEDADV003", ic50_nm: 7.0, off_target_ic50_nm: 320.0, clogp: 2.8, solubility_um: 65.0, permeability: 22.0, herg_ic50_um: 4.0, cyp_ic50_um: 18.0, assay_qc: 0.92 },
        Candidate { compound_id: "MEDADV006", ic50_nm: 32.0, off_target_ic50_nm: 5200.0, clogp: 1.9, solubility_um: 160.0, permeability: 26.0, herg_ic50_um: 42.0, cyp_ic50_um: 55.0, assay_qc: 0.95 },
    ];

    let mut file = File::create("../outputs/tables/rust_medicinal_candidate_scores.csv")?;
    writeln!(file, "compound_id,pIC50,LLE,selectivity_window,MPO_score,recommendation")?;

    for candidate in &candidates {
        writeln!(
            file,
            "{},{:.6},{:.6},{:.6},{:.6},{}",
            candidate.compound_id,
            pic50(candidate.ic50_nm),
            lle(candidate),
            selectivity(candidate),
            mpo(candidate),
            recommendation(candidate)
        )?;
    }

    println!("Rust medicinal candidate scoring complete.");
    Ok(())
}
