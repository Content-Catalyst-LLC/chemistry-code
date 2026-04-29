-- SQL schema for synthetic colloids, soft matter, and complex fluids records.
-- Educational only; adapt and validate before real formulation assessment.

CREATE TABLE IF NOT EXISTS colloid_system (
    formulation_id TEXT PRIMARY KEY,
    system_type TEXT NOT NULL,
    dispersed_phase TEXT,
    continuous_phase TEXT,
    particle_or_droplet_size_nm REAL,
    zeta_potential_mV REAL,
    volume_fraction REAL,
    low_shear_viscosity_Pa_s REAL,
    high_shear_viscosity_Pa_s REAL,
    yield_stress_Pa REAL,
    salt_aggregation_index REAL
);

CREATE TABLE IF NOT EXISTS rheology_replicate (
    formulation_id TEXT NOT NULL,
    replicate INTEGER NOT NULL,
    low_shear_viscosity_Pa_s REAL,
    high_shear_viscosity_Pa_s REAL,
    yield_stress_Pa REAL,
    salt_aggregation_index REAL,
    PRIMARY KEY (formulation_id, replicate),
    FOREIGN KEY (formulation_id) REFERENCES colloid_system(formulation_id)
);

CREATE TABLE IF NOT EXISTS stability_test (
    test_id TEXT PRIMARY KEY,
    formulation_id TEXT NOT NULL,
    condition TEXT,
    temperature_C REAL,
    storage_days REAL,
    phase_separation_index REAL,
    sedimentation_index REAL,
    creaming_index REAL,
    aggregation_flag INTEGER,
    FOREIGN KEY (formulation_id) REFERENCES colloid_system(formulation_id)
);

CREATE TABLE IF NOT EXISTS emulsion_property (
    emulsion_id TEXT PRIMARY KEY,
    formulation_id TEXT NOT NULL,
    oil_phase TEXT,
    surfactant_class TEXT,
    mean_droplet_size_nm REAL,
    polydispersity_index REAL,
    interfacial_tension_mN_m REAL,
    coalescence_index REAL,
    FOREIGN KEY (formulation_id) REFERENCES colloid_system(formulation_id)
);

CREATE TABLE IF NOT EXISTS gel_network (
    gel_id TEXT PRIMARY KEY,
    formulation_id TEXT NOT NULL,
    network_type TEXT,
    storage_modulus_Pa REAL,
    loss_modulus_Pa REAL,
    yield_stress_Pa REAL,
    recovery_after_shear_percent REAL,
    FOREIGN KEY (formulation_id) REFERENCES colloid_system(formulation_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    formulation_id TEXT NOT NULL,
    solvent_or_continuous_phase TEXT,
    additive_review_required INTEGER,
    particle_exposure_review TEXT,
    wastewater_fate_note TEXT,
    responsible_formulation_review INTEGER,
    FOREIGN KEY (formulation_id) REFERENCES colloid_system(formulation_id)
);
