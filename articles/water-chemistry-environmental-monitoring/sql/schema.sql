-- Water chemistry monitoring schema.
-- Educational SQL structure for provenance-aware water-quality data.
-- This schema is not a regulatory reporting template.

CREATE TABLE IF NOT EXISTS monitoring_sites (
    site_id TEXT PRIMARY KEY,
    site_name TEXT NOT NULL,
    medium TEXT NOT NULL,
    water_body_type TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS analytes (
    analyte_id TEXT PRIMARY KEY,
    analyte_name TEXT NOT NULL,
    analyte_group TEXT,
    default_unit TEXT NOT NULL,
    benchmark_value REAL,
    benchmark_unit TEXT,
    benchmark_context TEXT
);

CREATE TABLE IF NOT EXISTS samples (
    sample_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sample_date TEXT NOT NULL,
    pH REAL,
    temperature_c REAL,
    conductivity_uS_cm REAL,
    flow_L_s REAL,
    method TEXT,
    filtered BOOLEAN,
    qualifier TEXT,
    FOREIGN KEY (site_id) REFERENCES monitoring_sites(site_id)
);

CREATE TABLE IF NOT EXISTS measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    analyte_id TEXT NOT NULL,
    concentration REAL NOT NULL,
    unit TEXT NOT NULL,
    detection_limit REAL,
    reporting_limit REAL,
    uncertainty REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id),
    FOREIGN KEY (analyte_id) REFERENCES analytes(analyte_id)
);
