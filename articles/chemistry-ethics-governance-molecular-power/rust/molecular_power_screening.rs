// Chemistry, Ethics, and the Governance of Molecular Power
// Rust governance screening model.
// Synthetic educational code only.

use std::fs::{create_dir_all, File};
use std::io::{Result, Write};

#[derive(Debug)]
struct Record {
    domain: &'static str,
    context: &'static str,
    benefit: f64,
    hazard: f64,
    exposure: f64,
    vulnerability: f64,
    persistence: f64,
    irreversibility: f64,
    inequality: f64,
    worker: f64,
    dual_use: f64,
    transparency: f64,
    monitoring: f64,
    alternatives: f64,
    stewardship: f64,
    governance: f64,
    data: f64,
    qc: f64,
}

fn clamp01(x: f64) -> f64 {
    x.max(0.0).min(1.0)
}

fn chemical_risk(r: &Record) -> f64 {
    let baseline = r.hazard * r.exposure * r.vulnerability;
    let durable = 0.5 * r.persistence + 0.5 * r.irreversibility;
    clamp01(0.72 * baseline + 0.28 * durable)
}

fn justice_weighted_risk(r: &Record) -> f64 {
    clamp01(chemical_risk(r) * (1.0 + 0.50 * r.inequality + 0.35 * r.worker))
}

fn governance_gap(r: &Record) -> f64 {
    clamp01(justice_weighted_risk(r) * (1.0 - r.governance))
}

fn transparency_confidence(r: &Record) -> f64 {
    clamp01(0.40 * r.transparency + 0.30 * r.data + 0.20 * r.monitoring + 0.10 * r.qc)
}

fn stewardship_capacity(r: &Record) -> f64 {
    clamp01(0.35 * r.stewardship + 0.25 * r.governance + 0.20 * r.monitoring + 0.20 * r.alternatives)
}

fn responsible_score(r: &Record) -> f64 {
    clamp01(
        0.26 * r.benefit +
        0.22 * stewardship_capacity(r) +
        0.16 * transparency_confidence(r) +
        0.12 * r.alternatives -
        0.14 * justice_weighted_risk(r) -
        0.06 * r.dual_use -
        0.04 * governance_gap(r)
    )
}

fn flag(r: &Record) -> &'static str {
    if r.dual_use >= 0.80 {
        "restricted_or_high_dual_use_governance_attention"
    } else if governance_gap(r) >= 0.40 {
        "high_governance_gap"
    } else if justice_weighted_risk(r) >= 0.55 {
        "high_justice_weighted_risk"
    } else if responsible_score(r) >= 0.65 {
        "stronger_responsible_innovation_profile"
    } else {
        "monitor_and_improve_governance"
    }
}

fn main() -> Result<()> {
    create_dir_all("../outputs/tables").ok();

    let records = vec![
        Record { domain: "medicine", context: "essential_therapeutic", benefit: 0.95, hazard: 0.35, exposure: 0.42, vulnerability: 0.55, persistence: 0.30, irreversibility: 0.25, inequality: 0.22, worker: 0.30, dual_use: 0.05, transparency: 0.78, monitoring: 0.72, alternatives: 0.45, stewardship: 0.80, governance: 0.82, data: 0.88, qc: 0.94 },
        Record { domain: "agriculture", context: "high_volume_pesticide", benefit: 0.72, hazard: 0.68, exposure: 0.76, vulnerability: 0.84, persistence: 0.62, irreversibility: 0.50, inequality: 0.58, worker: 0.72, dual_use: 0.12, transparency: 0.45, monitoring: 0.50, alternatives: 0.62, stewardship: 0.48, governance: 0.55, data: 0.66, qc: 0.89 },
        Record { domain: "dual_use", context: "restricted_toxic_precursor", benefit: 0.22, hazard: 0.92, exposure: 0.35, vulnerability: 0.88, persistence: 0.60, irreversibility: 0.90, inequality: 0.52, worker: 0.68, dual_use: 0.95, transparency: 0.22, monitoring: 0.60, alternatives: 0.80, stewardship: 0.30, governance: 0.88, data: 0.74, qc: 0.90 },
    ];

    let mut file = File::create("../outputs/tables/rust_molecular_power_screening.csv")?;
    writeln!(file, "domain,context,chemical_risk,justice_weighted_risk,governance_gap,transparency_confidence,stewardship_capacity,responsible_score,flag")?;

    for r in &records {
        writeln!(
            file,
            "{},{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
            r.domain,
            r.context,
            chemical_risk(r),
            justice_weighted_risk(r),
            governance_gap(r),
            transparency_confidence(r),
            stewardship_capacity(r),
            responsible_score(r),
            flag(r)
        )?;
    }

    println!("Rust molecular power screening complete.");
    Ok(())
}
