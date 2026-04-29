-- SQL schema for synthetic chromatographic measurement records.
-- Educational only; adapt and validate before real laboratory use.

CREATE TABLE IF NOT EXISTS chromatographic_method (
    method_id TEXT PRIMARY KEY,
    method_type TEXT NOT NULL,
    instrument_id TEXT NOT NULL,
    column_id TEXT,
    mobile_phase_or_carrier TEXT,
    dead_time_min REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS chromatographic_peak (
    peak_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    method_id TEXT NOT NULL,
    retention_time_min REAL NOT NULL,
    baseline_width_min REAL NOT NULL,
    peak_area REAL NOT NULL,
    detector TEXT,
    FOREIGN KEY (method_id) REFERENCES chromatographic_method(method_id)
);

CREATE TABLE IF NOT EXISTS reference_compound (
    compound_id TEXT PRIMARY KEY,
    compound_name TEXT NOT NULL,
    reference_retention_time_min REAL NOT NULL,
    evidence_type TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS tentative_identification (
    identification_id TEXT PRIMARY KEY,
    peak_id TEXT NOT NULL,
    compound_id TEXT NOT NULL,
    retention_delta_min REAL NOT NULL,
    identification_status TEXT NOT NULL,
    caution_note TEXT,
    FOREIGN KEY (peak_id) REFERENCES chromatographic_peak(peak_id),
    FOREIGN KEY (compound_id) REFERENCES reference_compound(compound_id)
);

CREATE TABLE IF NOT EXISTS calibration_record (
    calibration_id TEXT PRIMARY KEY,
    compound_name TEXT NOT NULL,
    concentration_mg_l REAL,
    peak_area REAL NOT NULL,
    injection_id TEXT,
    record_type TEXT NOT NULL
);
