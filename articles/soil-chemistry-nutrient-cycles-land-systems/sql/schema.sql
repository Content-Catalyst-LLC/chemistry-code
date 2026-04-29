-- Soil chemistry monitoring schema.
-- Educational SQL structure for provenance-aware soil monitoring data.
-- This schema is not a regulatory, agronomic, or carbon-credit reporting template.

CREATE TABLE IF NOT EXISTS soil_sites (
    site_id TEXT PRIMARY KEY,
    site_name TEXT NOT NULL,
    land_use TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS soil_samples (
    sample_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sample_date TEXT NOT NULL,
    depth_cm REAL NOT NULL,
    bulk_density_g_cm3 REAL,
    method TEXT,
    qualifier TEXT,
    FOREIGN KEY (site_id) REFERENCES soil_sites(site_id)
);

CREATE TABLE IF NOT EXISTS soil_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    analyte TEXT NOT NULL,
    concentration REAL NOT NULL,
    unit TEXT NOT NULL,
    detection_limit REAL,
    reporting_limit REAL,
    uncertainty REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES soil_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS soil_exchange_properties (
    sample_id TEXT PRIMARY KEY,
    cec_cmolc_kg REAL,
    base_cations_cmolc_kg REAL,
    acidity_cmolc_kg REAL,
    FOREIGN KEY (sample_id) REFERENCES soil_samples(sample_id)
);
