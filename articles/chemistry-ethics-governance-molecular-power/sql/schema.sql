-- Chemistry, Ethics, and the Governance of Molecular Power
-- Synthetic educational schema only.
-- Not for legal, regulatory, toxicological, exposure, safety, security,
-- product-approval, or weapons-related determinations.

CREATE TABLE IF NOT EXISTS molecular_power_records (
    record_id TEXT PRIMARY KEY,
    chemical_domain TEXT,
    use_context TEXT,
    benefit_score REAL,
    hazard_score REAL,
    exposure_potential REAL,
    vulnerability_factor REAL,
    persistence_score REAL,
    irreversibility_score REAL,
    inequality_burden_score REAL,
    worker_exposure_score REAL,
    dual_use_concern REAL,
    transparency_score REAL,
    monitoring_score REAL,
    alternatives_score REAL,
    stewardship_score REAL,
    governance_strength REAL,
    data_completeness REAL,
    qc_score REAL
);

CREATE TABLE IF NOT EXISTS molecular_power_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT NOT NULL,
    chemical_risk REAL,
    justice_weighted_risk REAL,
    governance_gap REAL,
    transparency_confidence REAL,
    stewardship_capacity REAL,
    responsible_innovation_score REAL,
    governance_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (record_id) REFERENCES molecular_power_records(record_id)
);
