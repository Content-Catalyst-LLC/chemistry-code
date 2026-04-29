-- SQL schema for synthetic computational-notebook provenance in chemistry.
-- This schema is educational and should be adapted before use in regulated
-- laboratory, clinical, safety-critical, or environmental-compliance settings.

CREATE TABLE IF NOT EXISTS chemical_notebook_run (
    run_id TEXT PRIMARY KEY,
    notebook_id TEXT NOT NULL,
    molecule TEXT NOT NULL,
    method TEXT NOT NULL,
    instrument_id TEXT NOT NULL,
    environment_id TEXT NOT NULL,
    concentration_mol_l REAL NOT NULL,
    absorbance REAL NOT NULL,
    temperature_k REAL NOT NULL,
    analyst TEXT NOT NULL,
    random_seed INTEGER NOT NULL,
    execution_order INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notebook_environment (
    environment_id TEXT PRIMARY KEY,
    python_version TEXT,
    r_version TEXT,
    julia_version TEXT,
    operating_system TEXT,
    dependency_lockfile TEXT,
    container_image TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS provenance_artifact (
    artifact_id TEXT PRIMARY KEY,
    notebook_id TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum TEXT,
    description TEXT
);
