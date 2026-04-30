-- Ocean carbonate chemistry monitoring schema.
-- Educational SQL structure for provenance-aware ocean carbon data.
-- This schema is not a research cruise database, OCADS submission template,
-- or operational monitoring system.

CREATE TABLE IF NOT EXISTS ocean_stations (
    station_id TEXT PRIMARY KEY,
    station_name TEXT NOT NULL,
    region TEXT,
    water_type TEXT,
    latitude REAL,
    longitude REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS ocean_samples (
    sample_id TEXT PRIMARY KEY,
    station_id TEXT NOT NULL,
    sample_date TEXT NOT NULL,
    depth_m REAL,
    temperature_c REAL,
    salinity REAL,
    method TEXT,
    qualifier TEXT,
    FOREIGN KEY (station_id) REFERENCES ocean_stations(station_id)
);

CREATE TABLE IF NOT EXISTS carbonate_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    pH_total_scale REAL,
    DIC_umol_kg REAL,
    total_alkalinity_umol_kg REAL,
    pCO2_uatm REAL,
    calcium_mmol_kg REAL,
    oxygen_umol_kg REAL,
    nitrate_umol_kg REAL,
    phosphate_umol_kg REAL,
    silicate_umol_kg REAL,
    uncertainty_note TEXT,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES ocean_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS carbonate_indicators (
    sample_id TEXT PRIMARY KEY,
    carbonate_umol_kg_simplified REAL,
    omega_aragonite_simplified REAL,
    omega_calcite_simplified REAL,
    co2_flux_proxy_uatm REAL,
    saturation_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES ocean_samples(sample_id)
);
