-- SQL schema for synthetic materials chemistry records.
-- Educational only; adapt and validate before real materials selection or certification.

CREATE TABLE IF NOT EXISTS material_candidate (
    material_id TEXT PRIMARY KEY,
    material_class TEXT NOT NULL,
    density_g_cm3 REAL,
    modulus_GPa REAL,
    thermal_stability_C REAL,
    conductivity_S_m REAL,
    recyclability_score REAL,
    relative_cost_score REAL
);

CREATE TABLE IF NOT EXISTS processing_condition (
    process_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    synthesis_route TEXT,
    processing_temperature_C REAL,
    processing_time_h REAL,
    atmosphere TEXT,
    post_treatment TEXT,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);

CREATE TABLE IF NOT EXISTS property_measurement (
    measurement_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    property_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT,
    method TEXT,
    temperature_C REAL,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);

CREATE TABLE IF NOT EXISTS function_target (
    target_id TEXT PRIMARY KEY,
    application TEXT NOT NULL,
    density_g_cm3 REAL,
    modulus_GPa REAL,
    thermal_stability_C REAL,
    conductivity_S_m REAL,
    recyclability_score REAL,
    relative_cost_score REAL
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    material_id TEXT NOT NULL,
    critical_element_flag INTEGER,
    toxicity_flag TEXT,
    recyclability_note TEXT,
    processing_energy_note TEXT,
    end_of_life_note TEXT,
    FOREIGN KEY (material_id) REFERENCES material_candidate(material_id)
);
