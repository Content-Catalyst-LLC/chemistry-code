-- Advanced environmental chemistry provenance schema.
-- Educational only. Not a regulatory compliance database, public-health
-- advisory system, environmental forensic record, remediation design database,
-- legal record, ecological risk assessment, drinking-water determination,
-- hazardous-waste determination, or operational monitoring system.

CREATE TABLE IF NOT EXISTS environmental_sites (
    site_id TEXT PRIMARY KEY,
    site_name TEXT NOT NULL,
    compartment TEXT NOT NULL,
    matrix_type TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS environmental_samples (
    sample_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sample_date TEXT,
    pH REAL,
    temperature_c REAL,
    redox_Eh_mV REAL,
    dissolved_oxygen_mg_L REAL,
    flow_L_s REAL,
    water_depth_m REAL,
    bulk_density_g_cm3 REAL,
    porosity_fraction REAL,
    qc_score REAL,
    method_note TEXT,
    FOREIGN KEY (site_id) REFERENCES environmental_sites(site_id)
);

CREATE TABLE IF NOT EXISTS chemical_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    analyte TEXT NOT NULL,
    analyte_class TEXT,
    concentration REAL,
    benchmark REAL,
    unit TEXT,
    detection_limit REAL,
    reporting_limit REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES environmental_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS fate_transport_properties (
    sample_id TEXT PRIMARY KEY,
    organic_carbon_fraction REAL,
    koc_L_kg REAL,
    Kd_L_kg REAL,
    henry_atm_m3_mol REAL,
    half_life_days REAL,
    retardation_factor_proxy REAL,
    mobility_factor_proxy REAL,
    persistence_factor REAL,
    FOREIGN KEY (sample_id) REFERENCES environmental_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS environmental_advanced_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    benchmark_ratio REAL,
    load_kg_day REAL,
    pH_stress_index REAL,
    redox_stress_index REAL,
    oxygen_stress_index REAL,
    nutrient_pressure_index REAL,
    ionic_pressure_index REAL,
    contaminant_pressure_index REAL,
    chemical_habitability_pressure_index REAL,
    evidence_weighted_habitability_pressure REAL,
    monte_carlo_exceedance_probability REAL,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (sample_id) REFERENCES environmental_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS environmental_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    time_step REAL,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (sample_id) REFERENCES environmental_samples(sample_id)
);
