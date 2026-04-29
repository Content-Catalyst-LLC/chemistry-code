-- SQL schema for synthetic semiconductor, electronic, and photochemical materials records.
-- Educational only; adapt and validate before real device or materials assessment.

CREATE TABLE IF NOT EXISTS material_candidate (
    material_id TEXT PRIMARY KEY,
    material_class TEXT NOT NULL,
    band_gap_eV REAL,
    electron_mobility_cm2_V_s REAL,
    hole_mobility_cm2_V_s REAL,
    carrier_lifetime_ns REAL,
    absorption_edge_nm REAL,
    photostability_score REAL,
    processing_temperature_C REAL,
    critical_material_flag INTEGER
);

CREATE TABLE IF NOT EXISTS device_run (
    run_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    replicate INTEGER,
    photocurrent_mA_cm2 REAL,
    open_circuit_voltage_V REAL,
    fill_factor REAL,
    photostability_score REAL,
    measurement_condition TEXT,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);

CREATE TABLE IF NOT EXISTS photostability_time_series (
    material_id TEXT NOT NULL,
    illumination_hours REAL NOT NULL,
    normalized_performance REAL,
    stress_condition TEXT,
    PRIMARY KEY (material_id, illumination_hours),
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);

CREATE TABLE IF NOT EXISTS spectroscopy_measurement (
    measurement_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    method TEXT,
    absorption_peak_nm REAL,
    emission_peak_nm REAL,
    quantum_yield_relative REAL,
    excited_state_lifetime_ns REAL,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);

CREATE TABLE IF NOT EXISTS interface_record (
    interface_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    interface_type TEXT,
    dominant_issue TEXT,
    mitigation_strategy TEXT,
    review_required INTEGER,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    critical_material_flag INTEGER,
    toxicity_or_exposure_concern TEXT,
    processing_energy_review TEXT,
    end_of_life_note TEXT,
    responsible_design_review INTEGER,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);
