-- Astrochemical molecular survey schema.
-- Educational SQL structure for provenance-aware astrochemical data.
-- This schema is not a professional line-survey archive, mission database,
-- or molecular spectroscopy catalog.

CREATE TABLE IF NOT EXISTS astro_sources (
    source_id TEXT PRIMARY KEY,
    source_name TEXT NOT NULL,
    environment TEXT NOT NULL,
    distance_pc REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS molecular_species (
    species_id TEXT PRIMARY KEY,
    species_name TEXT NOT NULL,
    molecule_class TEXT,
    formula_text TEXT,
    reference_database TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS spectral_observations (
    observation_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    species_id TEXT NOT NULL,
    observation_date TEXT,
    rest_frequency_GHz REAL NOT NULL,
    observed_frequency_GHz REAL NOT NULL,
    integrated_intensity_K_km_s REAL,
    column_density_cm2 REAL,
    H2_column_density_cm2 REAL,
    dust_temperature_K REAL,
    gas_temperature_K REAL,
    uv_field_index REAL,
    telescope_band TEXT,
    method TEXT,
    qualifier TEXT,
    FOREIGN KEY (source_id) REFERENCES astro_sources(source_id),
    FOREIGN KEY (species_id) REFERENCES molecular_species(species_id)
);

CREATE TABLE IF NOT EXISTS astrochemical_indicators (
    observation_id TEXT PRIMARY KEY,
    radial_velocity_km_s REAL,
    photon_energy_J REAL,
    fractional_abundance REAL,
    desorption_rate_s1_simplified REAL,
    photodissociation_lifetime_years_simplified REAL,
    thermal_release_screen TEXT,
    photochemical_screen TEXT,
    FOREIGN KEY (observation_id) REFERENCES spectral_observations(observation_id)
);
