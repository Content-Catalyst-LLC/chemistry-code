-- Atmospheric chemistry monitoring schema.
-- Educational SQL structure for provenance-aware atmospheric data.
-- This schema is not a regulatory reporting template.

CREATE TABLE IF NOT EXISTS monitoring_sites (
    site_id TEXT PRIMARY KEY,
    site_name TEXT NOT NULL,
    site_type TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    altitude_m REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS analytes (
    analyte_id TEXT PRIMARY KEY,
    analyte_name TEXT NOT NULL,
    chemical_class TEXT NOT NULL,
    default_unit TEXT NOT NULL,
    reference_value REAL,
    reference_unit TEXT,
    reference_context TEXT
);

CREATE TABLE IF NOT EXISTS atmospheric_samples (
    sample_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sample_date TEXT NOT NULL,
    averaging_period TEXT,
    temperature_c REAL,
    relative_humidity_percent REAL,
    wind_speed_m_s REAL,
    method TEXT,
    qualifier TEXT,
    FOREIGN KEY (site_id) REFERENCES monitoring_sites(site_id)
);

CREATE TABLE IF NOT EXISTS atmospheric_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    analyte_id TEXT NOT NULL,
    concentration REAL NOT NULL,
    unit TEXT NOT NULL,
    detection_limit REAL,
    uncertainty REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES atmospheric_samples(sample_id),
    FOREIGN KEY (analyte_id) REFERENCES analytes(analyte_id)
);
