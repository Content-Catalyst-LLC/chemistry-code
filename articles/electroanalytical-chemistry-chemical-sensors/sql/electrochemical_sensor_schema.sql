-- SQL schema for synthetic electroanalytical sensor records.
-- Educational only; adapt and validate before real laboratory or field use.

CREATE TABLE IF NOT EXISTS electrochemical_method (
    method_id TEXT PRIMARY KEY,
    method_name TEXT NOT NULL,
    instrument_id TEXT NOT NULL,
    electrode_id TEXT NOT NULL,
    electrode_material TEXT,
    reference_electrode TEXT,
    electrolyte TEXT,
    pH REAL,
    temperature_K REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS amperometric_calibration (
    standard_id TEXT PRIMARY KEY,
    method_id TEXT,
    analyte TEXT NOT NULL,
    concentration_uM REAL NOT NULL,
    current_uA REAL NOT NULL,
    electrode_id TEXT,
    FOREIGN KEY (method_id) REFERENCES electrochemical_method(method_id)
);

CREATE TABLE IF NOT EXISTS sensor_unknown (
    measurement_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    replicate_id TEXT,
    current_uA REAL NOT NULL,
    estimated_concentration_uM REAL,
    electrode_id TEXT,
    matrix TEXT
);

CREATE TABLE IF NOT EXISTS sensor_drift_record (
    drift_id TEXT PRIMARY KEY,
    time_min REAL NOT NULL,
    sample_id TEXT NOT NULL,
    current_uA REAL NOT NULL,
    electrode_id TEXT,
    condition TEXT
);

CREATE TABLE IF NOT EXISTS interference_test (
    test_id TEXT PRIMARY KEY,
    target_concentration_uM REAL,
    interferent TEXT,
    interferent_concentration_uM REAL,
    current_uA REAL,
    response_change_percent REAL
);

CREATE TABLE IF NOT EXISTS voltammetric_peak (
    scan_id TEXT PRIMARY KEY,
    analyte TEXT NOT NULL,
    peak_potential_V REAL,
    peak_current_uA REAL,
    scan_rate_mV_s REAL,
    electrode_id TEXT
);
