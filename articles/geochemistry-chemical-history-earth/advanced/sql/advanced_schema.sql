-- Advanced geochemistry provenance schema.
-- Educational only. Not a professional geochemical database, mining database,
-- geochronology report, contamination assessment, legal record, or resource estimate.

CREATE TABLE IF NOT EXISTS geochemical_samples (
    sample_id TEXT PRIMARY KEY,
    sample_date TEXT,
    location TEXT,
    material TEXT,
    rock_type TEXT,
    geologic_context TEXT,
    method_note TEXT,
    qc_score REAL
);

CREATE TABLE IF NOT EXISTS major_oxide_measurements (
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

CREATE TABLE IF NOT EXISTS trace_element_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    element_symbol TEXT NOT NULL,
    concentration_ppm REAL,
    detection_limit_ppm REAL,
    uncertainty_ppm REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS isotope_measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    isotope_system TEXT NOT NULL,
    sample_ratio REAL,
    standard_ratio REAL,
    delta_permil REAL,
    standard_name TEXT,
    uncertainty_permil REAL,
    qc_flag TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS geochemical_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    CIA_weight_based REAL,
    CIA_molar_CaO_star REAL,
    Rb_Sr_ratio REAL,
    Th_U_ratio REAL,
    Zr_Y_ratio REAL,
    LaN_YbN_ratio REAL,
    redox_archive_index REAL,
    geochemical_archive_index REAL,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);

CREATE TABLE IF NOT EXISTS radiometric_model_outputs (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT,
    parent_isotope_units REAL,
    radiogenic_daughter_units REAL,
    decay_constant_per_year REAL,
    age_Ma_simplified REAL,
    assumption_note TEXT,
    FOREIGN KEY (sample_id) REFERENCES geochemical_samples(sample_id)
);
