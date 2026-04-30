-- Advanced toxicology and exposure provenance schema.
-- Educational only. Not a regulatory compliance database, clinical system,
-- public-health advisory system, causation analysis, legal record,
-- cleanup decision system, or occupational safety determination.

CREATE TABLE IF NOT EXISTS toxicology_chemicals (
    chemical_id TEXT PRIMARY KEY,
    chemical_name TEXT NOT NULL,
    chemical_class TEXT,
    mixture_group TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS exposure_records (
    record_id TEXT PRIMARY KEY,
    chemical_id TEXT NOT NULL,
    medium TEXT,
    route TEXT,
    target_system TEXT,
    effect_type TEXT,
    concentration REAL,
    unit TEXT,
    intake_rate REAL,
    body_weight_kg REAL,
    exposure_frequency_days_year REAL,
    exposure_duration_years REAL,
    averaging_time_days REAL,
    absorption_fraction REAL,
    exposure_quality_score REAL,
    vulnerability_factor REAL,
    FOREIGN KEY (chemical_id) REFERENCES toxicology_chemicals(chemical_id)
);

CREATE TABLE IF NOT EXISTS toxicity_values (
    toxicity_value_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chemical_id TEXT NOT NULL,
    reference_dose_mg_kg_day REAL,
    slope_factor_per_mg_kg_day REAL,
    point_of_departure_mg_kg_day REAL,
    basis_note TEXT,
    uncertainty_note TEXT,
    FOREIGN KEY (chemical_id) REFERENCES toxicology_chemicals(chemical_id)
);

CREATE TABLE IF NOT EXISTS toxicology_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT NOT NULL,
    chronic_daily_intake_mg_kg_day REAL,
    absorbed_dose_mg_kg_day REAL,
    hazard_quotient REAL,
    vulnerability_adjusted_hazard REAL,
    margin_of_exposure REAL,
    cancer_risk_proxy REAL,
    evidence_weighted_risk_index REAL,
    mc_probability_hq_above_1 REAL,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (record_id) REFERENCES exposure_records(record_id)
);

CREATE TABLE IF NOT EXISTS toxicology_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (record_id) REFERENCES exposure_records(record_id)
);
