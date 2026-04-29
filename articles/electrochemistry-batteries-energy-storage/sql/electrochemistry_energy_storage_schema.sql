-- SQL schema for synthetic electrochemistry, battery, and energy-storage records.
-- Educational only; adapt and validate before real energy-storage assessment.

CREATE TABLE IF NOT EXISTS cell_candidate (
    cell_id TEXT PRIMARY KEY,
    chemistry TEXT NOT NULL,
    nominal_voltage_V REAL,
    specific_capacity_mAh_g REAL,
    active_material_mass_g REAL,
    cycle_100_capacity_retention REAL,
    coulombic_efficiency REAL,
    rate_capability_score REAL,
    critical_material_score REAL,
    safety_review_score REAL
);

CREATE TABLE IF NOT EXISTS cycling_data (
    cell_id TEXT NOT NULL,
    cycle_number INTEGER NOT NULL,
    discharge_capacity_mAh REAL,
    charge_capacity_mAh REAL,
    temperature_C REAL,
    current_rate_C REAL,
    PRIMARY KEY (cell_id, cycle_number),
    FOREIGN KEY (cell_id) REFERENCES cell_candidate(cell_id)
);

CREATE TABLE IF NOT EXISTS voltage_profile (
    profile_id TEXT PRIMARY KEY,
    cell_id TEXT NOT NULL,
    state_of_charge_percent REAL,
    voltage_V REAL,
    discharge_current_A REAL,
    FOREIGN KEY (cell_id) REFERENCES cell_candidate(cell_id)
);

CREATE TABLE IF NOT EXISTS impedance_measurement (
    measurement_id TEXT PRIMARY KEY,
    cell_id TEXT NOT NULL,
    cycle_number INTEGER,
    ohmic_resistance_mOhm REAL,
    charge_transfer_resistance_mOhm REAL,
    diffusion_tail_score REAL,
    FOREIGN KEY (cell_id) REFERENCES cell_candidate(cell_id)
);

CREATE TABLE IF NOT EXISTS materials_inventory (
    material_id TEXT PRIMARY KEY,
    cell_id TEXT NOT NULL,
    component TEXT,
    material_name TEXT,
    critical_material_flag INTEGER,
    recycling_priority TEXT,
    exposure_or_safety_note TEXT,
    FOREIGN KEY (cell_id) REFERENCES cell_candidate(cell_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    cell_id TEXT NOT NULL,
    critical_material_review INTEGER,
    safety_review_required INTEGER,
    recycling_pathway TEXT,
    end_of_life_note TEXT,
    responsible_design_review INTEGER,
    FOREIGN KEY (cell_id) REFERENCES cell_candidate(cell_id)
);
