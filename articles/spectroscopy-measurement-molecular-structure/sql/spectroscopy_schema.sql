-- SQL schema for synthetic spectroscopic measurement records.
-- Educational only; adapt and validate before real laboratory use.

CREATE TABLE IF NOT EXISTS spectral_sample (
    sample_id TEXT PRIMARY KEY,
    description TEXT,
    matrix_or_solvent TEXT,
    responsible_use_note TEXT
);

CREATE TABLE IF NOT EXISTS spectral_measurement (
    measurement_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    method TEXT NOT NULL,
    instrument_id TEXT NOT NULL,
    operator TEXT,
    temperature_k REAL,
    acquisition_notes TEXT,
    FOREIGN KEY (sample_id) REFERENCES spectral_sample(sample_id)
);

CREATE TABLE IF NOT EXISTS ir_peak (
    peak_id TEXT PRIMARY KEY,
    measurement_id TEXT NOT NULL,
    wavenumber_cm_minus_1 REAL NOT NULL,
    relative_intensity REAL NOT NULL,
    educational_assignment TEXT,
    FOREIGN KEY (measurement_id) REFERENCES spectral_measurement(measurement_id)
);

CREATE TABLE IF NOT EXISTS uvvis_measurement (
    record_id TEXT PRIMARY KEY,
    measurement_id TEXT NOT NULL,
    concentration_mol_l REAL,
    absorbance REAL NOT NULL,
    wavelength_nm REAL NOT NULL,
    path_length_cm REAL NOT NULL,
    FOREIGN KEY (measurement_id) REFERENCES spectral_measurement(measurement_id)
);

CREATE TABLE IF NOT EXISTS nmr_signal (
    signal_id TEXT PRIMARY KEY,
    measurement_id TEXT NOT NULL,
    chemical_shift_ppm REAL NOT NULL,
    integration REAL,
    multiplicity TEXT,
    educational_region TEXT,
    FOREIGN KEY (measurement_id) REFERENCES spectral_measurement(measurement_id)
);
