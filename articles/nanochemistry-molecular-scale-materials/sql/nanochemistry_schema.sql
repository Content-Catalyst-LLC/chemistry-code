-- SQL schema for synthetic nanochemistry records.
-- Educational only; adapt and validate before real nanomaterial assessment.

CREATE TABLE IF NOT EXISTS nanomaterial_candidate (
    sample_id TEXT PRIMARY KEY,
    material_class TEXT NOT NULL,
    core_diameter_nm REAL,
    hydrodynamic_diameter_nm REAL,
    zeta_potential_mV REAL,
    polydispersity_index REAL,
    ligand_coverage_relative REAL,
    aggregation_after_salt_relative REAL,
    critical_material_flag INTEGER
);

CREATE TABLE IF NOT EXISTS nanoparticle_replicate (
    sample_id TEXT NOT NULL,
    replicate INTEGER NOT NULL,
    core_diameter_nm REAL,
    hydrodynamic_diameter_nm REAL,
    polydispersity_index REAL,
    aggregation_after_salt_relative REAL,
    PRIMARY KEY (sample_id, replicate),
    FOREIGN KEY (sample_id) REFERENCES nanomaterial_candidate(sample_id)
);

CREATE TABLE IF NOT EXISTS ligand_shell (
    ligand_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    ligand_class TEXT,
    functional_group TEXT,
    coverage_relative REAL,
    solvent_compatibility TEXT,
    stabilization_mode TEXT,
    FOREIGN KEY (sample_id) REFERENCES nanomaterial_candidate(sample_id)
);

CREATE TABLE IF NOT EXISTS optical_property (
    sample_id TEXT PRIMARY KEY,
    material_class TEXT,
    core_diameter_nm REAL,
    absorbance_peak_nm REAL,
    emission_peak_nm REAL,
    quantum_yield_relative REAL,
    photostability_relative REAL,
    FOREIGN KEY (sample_id) REFERENCES nanomaterial_candidate(sample_id)
);

CREATE TABLE IF NOT EXISTS stability_media_test (
    test_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    medium TEXT,
    pH REAL,
    ionic_strength_mM REAL,
    hydrodynamic_diameter_after_h_nm REAL,
    aggregation_flag INTEGER,
    FOREIGN KEY (sample_id) REFERENCES nanomaterial_candidate(sample_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    critical_material_flag INTEGER,
    dissolution_or_transformation_concern TEXT,
    exposure_review_required TEXT,
    end_of_life_note TEXT,
    FOREIGN KEY (sample_id) REFERENCES nanomaterial_candidate(sample_id)
);
