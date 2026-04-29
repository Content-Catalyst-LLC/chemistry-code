-- SQL schema for synthetic mass spectrometry records.
-- Educational only; adapt and validate before real laboratory use.

CREATE TABLE IF NOT EXISTS ms_method (
    method_id TEXT PRIMARY KEY,
    method_name TEXT NOT NULL,
    instrument_id TEXT NOT NULL,
    analyzer TEXT,
    ionization TEXT,
    mass_range_mz TEXT,
    resolution_setting TEXT,
    chromatography TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS ms_feature (
    feature_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    method_id TEXT,
    retention_time_min REAL,
    observed_mz REAL NOT NULL,
    charge INTEGER,
    peak_area REAL,
    ion_mode TEXT,
    adduct TEXT,
    FOREIGN KEY (method_id) REFERENCES ms_method(method_id)
);

CREATE TABLE IF NOT EXISTS ms_candidate (
    candidate_id TEXT PRIMARY KEY,
    candidate_name TEXT NOT NULL,
    theoretical_mz REAL NOT NULL,
    expected_charge INTEGER,
    ion_mode TEXT,
    evidence_note TEXT
);

CREATE TABLE IF NOT EXISTS ms_candidate_match (
    match_id TEXT PRIMARY KEY,
    feature_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    ppm_error REAL NOT NULL,
    identification_status TEXT NOT NULL,
    caution_note TEXT,
    FOREIGN KEY (feature_id) REFERENCES ms_feature(feature_id),
    FOREIGN KEY (candidate_id) REFERENCES ms_candidate(candidate_id)
);

CREATE TABLE IF NOT EXISTS msms_fragment (
    fragment_id TEXT PRIMARY KEY,
    feature_id TEXT NOT NULL,
    precursor_mz REAL NOT NULL,
    product_mz REAL NOT NULL,
    relative_intensity REAL,
    collision_energy_ev REAL,
    fragment_note TEXT,
    FOREIGN KEY (feature_id) REFERENCES ms_feature(feature_id)
);

CREATE TABLE IF NOT EXISTS ms_calibration_record (
    calibration_id TEXT PRIMARY KEY,
    compound_name TEXT NOT NULL,
    concentration_ng_ml REAL,
    peak_area REAL NOT NULL,
    injection_id TEXT,
    record_type TEXT NOT NULL
);
