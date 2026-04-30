-- Advanced astrochemistry provenance schema.
-- Educational only. Not a professional observatory archive or spectroscopy database.

CREATE TABLE IF NOT EXISTS molecular_catalog_lines (
    catalog_line_id INTEGER PRIMARY KEY AUTOINCREMENT,
    species TEXT NOT NULL,
    transition_label TEXT NOT NULL,
    rest_frequency_GHz REAL NOT NULL,
    upper_energy_K REAL,
    einstein_A_s1 REAL,
    g_upper REAL,
    molecule_class TEXT,
    catalog_source TEXT,
    uncertainty_MHz REAL
);

CREATE TABLE IF NOT EXISTS observed_spectral_lines (
    observed_line_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    environment TEXT,
    observed_frequency_GHz REAL NOT NULL,
    peak_intensity_K REAL,
    line_width_km_s REAL,
    integrated_intensity_K_km_s REAL,
    noise_K REAL,
    observation_date TEXT,
    telescope_band TEXT,
    velocity_frame TEXT,
    calibration_note TEXT
);

CREATE TABLE IF NOT EXISTS line_match_results (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    observed_line_id INTEGER NOT NULL,
    catalog_line_id INTEGER NOT NULL,
    frequency_offset_MHz REAL,
    radial_velocity_km_s REAL,
    signal_to_noise REAL,
    match_quality TEXT,
    notes TEXT,
    FOREIGN KEY (observed_line_id) REFERENCES observed_spectral_lines(observed_line_id),
    FOREIGN KEY (catalog_line_id) REFERENCES molecular_catalog_lines(catalog_line_id)
);

CREATE TABLE IF NOT EXISTS rotational_diagram_results (
    rotational_result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    species TEXT NOT NULL,
    rotational_temperature_K REAL,
    slope REAL,
    intercept REAL,
    n_transitions INTEGER,
    assumptions TEXT
);

CREATE TABLE IF NOT EXISTS astrochemical_model_runs (
    model_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    run_date TEXT,
    network_description TEXT,
    integration_method TEXT,
    time_end_years REAL,
    time_step_years REAL,
    assumptions TEXT,
    responsible_use_note TEXT
);
