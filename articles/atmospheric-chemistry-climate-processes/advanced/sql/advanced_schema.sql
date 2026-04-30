-- Advanced atmospheric chemistry provenance schema.
-- Educational only. Not a regulatory air-quality database, chemical transport
-- model archive, public-health advisory system, climate-attribution database,
-- emissions inventory, legal record, or operational forecast system.

CREATE TABLE IF NOT EXISTS atmospheric_stations (
    station_id TEXT PRIMARY KEY,
    station_name TEXT NOT NULL,
    region TEXT,
    environment TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS atmospheric_observations (
    observation_id TEXT PRIMARY KEY,
    station_id TEXT NOT NULL,
    observation_date TEXT,
    species TEXT NOT NULL,
    chemical_class TEXT,
    concentration REAL,
    reference_concentration REAL,
    unit TEXT,
    temperature_c REAL,
    relative_humidity_percent REAL,
    background_pressure_hPa REAL,
    qc_score REAL,
    method_note TEXT,
    FOREIGN KEY (station_id) REFERENCES atmospheric_stations(station_id)
);

CREATE TABLE IF NOT EXISTS atmospheric_context (
    observation_id TEXT PRIMARY KEY,
    sunlight_index REAL,
    nox_ppb REAL,
    voc_ppb REAL,
    oh_index REAL,
    aod REAL,
    single_scattering_albedo REAL,
    lifetime_days REAL,
    FOREIGN KEY (observation_id) REFERENCES atmospheric_observations(observation_id)
);

CREATE TABLE IF NOT EXISTS atmospheric_advanced_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    observation_id TEXT NOT NULL,
    reference_ratio REAL,
    greenhouse_forcing_proxy_W_m2 REAL,
    lifetime_persistence_factor REAL,
    photochemical_ozone_index REAL,
    aerosol_direct_effect_proxy REAL,
    aerosol_pressure_index REAL,
    oxidizing_capacity_stress_index REAL,
    atmospheric_chemistry_pressure_index REAL,
    evidence_weighted_pressure_index REAL,
    attention_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (observation_id) REFERENCES atmospheric_observations(observation_id)
);

CREATE TABLE IF NOT EXISTS atmospheric_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    observation_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    time_step REAL,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (observation_id) REFERENCES atmospheric_observations(observation_id)
);
