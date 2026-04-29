-- SQL schema for synthetic polymer chemistry records.
-- Educational only; adapt and validate before real polymer selection or certification.

CREATE TABLE IF NOT EXISTS polymer_candidate (
    polymer_id TEXT PRIMARY KEY,
    polymer_class TEXT NOT NULL,
    glass_transition_C REAL,
    melting_temperature_C REAL,
    crystallinity_percent REAL,
    oxygen_permeability_relative REAL,
    modulus_MPa REAL,
    elongation_percent REAL,
    recyclability_score REAL,
    relative_cost_score REAL
);

CREATE TABLE IF NOT EXISTS molar_mass_fraction (
    polymer_id TEXT NOT NULL,
    fraction_id TEXT NOT NULL,
    molecule_count REAL NOT NULL,
    molar_mass_g_mol REAL NOT NULL,
    PRIMARY KEY (polymer_id, fraction_id),
    FOREIGN KEY (polymer_id) REFERENCES polymer_candidate(polymer_id)
);

CREATE TABLE IF NOT EXISTS processing_condition (
    process_id TEXT PRIMARY KEY,
    polymer_id TEXT NOT NULL,
    polymerization_route TEXT,
    processing_method TEXT,
    processing_temperature_C REAL,
    processing_time_h REAL,
    atmosphere TEXT,
    post_treatment TEXT,
    FOREIGN KEY (polymer_id) REFERENCES polymer_candidate(polymer_id)
);

CREATE TABLE IF NOT EXISTS property_measurement (
    measurement_id TEXT PRIMARY KEY,
    polymer_id TEXT NOT NULL,
    property_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT,
    method TEXT,
    temperature_C REAL,
    FOREIGN KEY (polymer_id) REFERENCES polymer_candidate(polymer_id)
);

CREATE TABLE IF NOT EXISTS degradation_lifecycle_note (
    note_id TEXT PRIMARY KEY,
    polymer_id TEXT NOT NULL,
    hydrolysis_sensitive TEXT,
    oxidation_sensitive TEXT,
    uv_sensitive TEXT,
    recycling_pathway TEXT,
    biodegradation_claim_status TEXT,
    additive_or_leachable_note TEXT,
    FOREIGN KEY (polymer_id) REFERENCES polymer_candidate(polymer_id)
);

CREATE TABLE IF NOT EXISTS function_target (
    target_id TEXT PRIMARY KEY,
    application TEXT NOT NULL,
    oxygen_permeability_relative REAL,
    modulus_MPa REAL,
    elongation_percent REAL,
    recyclability_score REAL,
    relative_cost_score REAL
);
