-- Advanced ocean carbonate chemistry provenance schema.
-- Educational only. Not an OCADS submission template, regulatory database,
-- research cruise archive, or operational ocean-acidification system.

CREATE TABLE IF NOT EXISTS ocean_carbonate_samples (
    sample_id TEXT PRIMARY KEY,
    sample_date TEXT,
    station TEXT NOT NULL,
    region TEXT,
    water_type TEXT,
    depth_m REAL,
    temperature_c REAL,
    salinity REAL,
    method_note TEXT,
    qc_score REAL
);

CREATE TABLE IF NOT EXISTS carbonate_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    pH_total_scale REAL,
    DIC_umol_kg REAL,
    total_alkalinity_umol_kg REAL,
    pCO2_water_uatm REAL,
    pCO2_air_uatm REAL,
    calcium_mmol_kg REAL,
    oxygen_umol_kg REAL,
    nitrate_umol_kg REAL,
    phosphate_umol_kg REAL,
    silicate_umol_kg REAL,
    wind_speed_m_s REAL,
    FOREIGN KEY (sample_id) REFERENCES ocean_carbonate_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS carbonate_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    CO2_star_umol_kg REAL,
    bicarbonate_umol_kg REAL,
    carbonate_umol_kg REAL,
    omega_aragonite_simplified REAL,
    omega_calcite_simplified REAL,
    alkalinity_DIC_buffer_ratio REAL,
    air_sea_CO2_flux_proxy REAL,
    revelle_factor_intuition_proxy REAL,
    acidification_pressure_index REAL,
    saturation_flag TEXT,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (sample_id) REFERENCES ocean_carbonate_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS carbonate_sensitivity_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    added_DIC_umol_kg REAL,
    modeled_pH_total_scale REAL,
    modeled_carbonate_umol_kg REAL,
    modeled_omega_aragonite REAL,
    assumption_note TEXT,
    FOREIGN KEY (sample_id) REFERENCES ocean_carbonate_samples(sample_id)
);
