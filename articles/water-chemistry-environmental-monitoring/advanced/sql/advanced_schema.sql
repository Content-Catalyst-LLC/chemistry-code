-- Advanced water chemistry provenance schema.
-- Educational only. Not a regulatory compliance database, drinking-water
-- safety system, public-health advisory system, legal record, watershed
-- permit model, or operational monitoring database.

CREATE TABLE IF NOT EXISTS water_sites (
    site_id TEXT PRIMARY KEY,
    site_name TEXT NOT NULL,
    medium TEXT NOT NULL,
    water_body_type TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS water_samples (
    sample_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sample_date TEXT,
    temperature_c REAL,
    pH REAL,
    specific_conductance_uS_cm REAL,
    flow_L_s REAL,
    qc_score REAL,
    method_note TEXT,
    FOREIGN KEY (site_id) REFERENCES water_sites(site_id)
);

CREATE TABLE IF NOT EXISTS water_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    analyte TEXT NOT NULL,
    concentration REAL,
    benchmark REAL,
    unit TEXT,
    detection_limit REAL,
    reporting_limit REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES water_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS water_advanced_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    benchmark_ratio REAL,
    load_kg_day REAL,
    oxygen_deficit_mg_L REAL,
    oxygen_stress_index REAL,
    nutrient_enrichment_index REAL,
    metal_pressure_index REAL,
    turbidity_pressure REAL,
    conductivity_pressure REAL,
    chloride_pressure REAL,
    pH_pressure REAL,
    water_quality_pressure_index REAL,
    evidence_weighted_pressure_index REAL,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (sample_id) REFERENCES water_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS water_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    time_step REAL,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (sample_id) REFERENCES water_samples(sample_id)
);
