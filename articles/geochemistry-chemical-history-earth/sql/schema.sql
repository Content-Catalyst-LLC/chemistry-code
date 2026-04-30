-- Geochemical sample schema.
-- Educational SQL structure for provenance-aware geochemical data.
-- This schema is not a professional laboratory information management system.

CREATE TABLE IF NOT EXISTS geochemical_samples (
    sample_id TEXT PRIMARY KEY,
    sample_date TEXT,
    location TEXT,
    material TEXT,
    rock_type TEXT,
    geologic_context TEXT,
    latitude REAL,
    longitude REAL,
    method TEXT,
    qualifier TEXT
);

CREATE TABLE IF NOT EXISTS major_oxides (
    sample_id TEXT PRIMARY KEY,
    SiO2_wt_pct REAL,
    Al2O3_wt_pct REAL,
    FeO_total_wt_pct REAL,
    MgO_wt_pct REAL,
    CaO_wt_pct REAL,
    Na2O_wt_pct REAL,
    K2O_wt_pct REAL,
    TiO2_wt_pct REAL,
    P2O5_wt_pct REAL,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS trace_elements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    element_symbol TEXT NOT NULL,
    concentration_ppm REAL NOT NULL,
    detection_limit_ppm REAL,
    uncertainty_ppm REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS isotope_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    isotope_system TEXT NOT NULL,
    ratio_or_delta_value REAL NOT NULL,
    unit TEXT NOT NULL,
    standard_name TEXT,
    uncertainty REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS radiometric_systems (
    sample_id TEXT PRIMARY KEY,
    parent_isotope_units REAL,
    radiogenic_daughter_units REAL,
    decay_constant_per_year REAL,
    age_Ma_simplified REAL,
    interpretation_notes TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);
