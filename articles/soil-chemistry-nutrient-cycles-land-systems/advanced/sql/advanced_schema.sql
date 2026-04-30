-- Advanced soil chemistry provenance schema.
-- Educational only. Not an agronomic recommendation database, soil-carbon
-- credit registry, contamination assessment, public-health advisory system,
-- legal record, or regulatory reporting database.

CREATE TABLE IF NOT EXISTS soil_sites (
    site_id TEXT PRIMARY KEY,
    site_name TEXT NOT NULL,
    land_use TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS soil_samples (
    sample_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sample_date TEXT,
    depth_cm REAL,
    bulk_density_g_cm3 REAL,
    qc_score REAL,
    method_note TEXT,
    FOREIGN KEY (site_id) REFERENCES soil_sites(site_id)
);

CREATE TABLE IF NOT EXISTS soil_chemical_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    analyte TEXT NOT NULL,
    value REAL,
    unit TEXT,
    method_note TEXT,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES soil_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS soil_exchange_properties (
    sample_id TEXT PRIMARY KEY,
    cec_cmolc_kg REAL,
    base_cations_cmolc_kg REAL,
    base_saturation_percent REAL,
    exchange_acidity_proxy_cmolc_kg REAL,
    FOREIGN KEY (sample_id) REFERENCES soil_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS soil_advanced_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    soc_stock_Mg_ha REAL,
    equivalent_soil_mass_proxy_Mg_ha REAL,
    nitrate_leaching_vulnerability REAL,
    phosphorus_export_kg_ha_proxy REAL,
    annual_N_balance_kg_ha REAL,
    annual_P_balance_kg_ha REAL,
    pH_pressure REAL,
    salinity_pressure REAL,
    contaminant_pressure REAL,
    soil_land_system_pressure_index REAL,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (sample_id) REFERENCES soil_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS soil_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    scenario_year INTEGER,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (sample_id) REFERENCES soil_samples(sample_id)
);
