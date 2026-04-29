-- SQL schema for synthetic surface chemistry and catalysis records.
-- Educational only; adapt and validate before real catalyst design or process use.

CREATE TABLE IF NOT EXISTS catalyst_candidate (
    catalyst_id TEXT PRIMARY KEY,
    catalyst_class TEXT NOT NULL,
    surface_area_m2_g REAL,
    site_density_umol_g REAL,
    K_A_bar_inv REAL,
    K_B_bar_inv REAL,
    activation_energy_kJ_mol REAL,
    selectivity_target REAL,
    critical_metal_flag INTEGER
);

CREATE TABLE IF NOT EXISTS adsorption_isotherm (
    experiment_id TEXT PRIMARY KEY,
    catalyst_id TEXT NOT NULL,
    adsorbate TEXT NOT NULL,
    pressure_bar REAL,
    coverage_fraction REAL,
    temperature_K REAL,
    FOREIGN KEY (catalyst_id) REFERENCES catalyst_candidate(catalyst_id)
);

CREATE TABLE IF NOT EXISTS catalyst_performance (
    run_id TEXT PRIMARY KEY,
    catalyst_id TEXT NOT NULL,
    replicate INTEGER,
    conversion_percent REAL,
    selectivity_percent REAL,
    temperature_K REAL,
    time_on_stream_h REAL,
    FOREIGN KEY (catalyst_id) REFERENCES catalyst_candidate(catalyst_id)
);

CREATE TABLE IF NOT EXISTS deactivation_time_series (
    catalyst_id TEXT NOT NULL,
    time_h REAL NOT NULL,
    normalized_rate REAL NOT NULL,
    condition TEXT,
    PRIMARY KEY (catalyst_id, time_h),
    FOREIGN KEY (catalyst_id) REFERENCES catalyst_candidate(catalyst_id)
);

CREATE TABLE IF NOT EXISTS surface_characterization (
    measurement_id TEXT PRIMARY KEY,
    catalyst_id TEXT NOT NULL,
    method TEXT,
    measurement_target TEXT,
    value REAL,
    unit TEXT,
    condition TEXT,
    FOREIGN KEY (catalyst_id) REFERENCES catalyst_candidate(catalyst_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    catalyst_id TEXT NOT NULL,
    critical_material_flag INTEGER,
    toxicity_flag TEXT,
    regeneration_note TEXT,
    end_of_life_note TEXT,
    sustainability_review_required INTEGER,
    FOREIGN KEY (catalyst_id) REFERENCES catalyst_candidate(catalyst_id)
);

CREATE TABLE IF NOT EXISTS interface_record (
    interface_id TEXT PRIMARY KEY,
    system TEXT,
    phase_boundary TEXT,
    dominant_interaction TEXT,
    measurement_method TEXT,
    application_context TEXT
);
