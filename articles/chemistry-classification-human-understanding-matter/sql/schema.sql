-- Chemistry, Classification, and the Human Understanding of Matter
-- Synthetic educational schema only.
-- Not for real unknown identification, regulatory classification, safety data sheets,
-- purity certification, or analytical validation.

CREATE TABLE IF NOT EXISTS chemical_records (
    record_id TEXT PRIMARY KEY,
    sample_name TEXT NOT NULL,
    components REAL,
    phase TEXT,
    molecular_weight REAL,
    charge REAL,
    contains_metal INTEGER,
    coordination_number REAL,
    is_polymer INTEGER,
    network_structure INTEGER,
    organic_fraction REAL,
    ionic_fraction REAL,
    metallic_fraction REAL,
    crystalline_score REAL,
    functional_group TEXT,
    spectral_match_score REAL,
    elemental_match_score REAL,
    thermal_signature_score REAL,
    hazard_indicator_score REAL,
    classification_confidence REAL,
    qc_score REAL
);

CREATE TABLE IF NOT EXISTS chemical_classification_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id TEXT NOT NULL,
    assigned_class TEXT,
    evidence_score REAL,
    classification_reliability REAL,
    hazard_triage TEXT,
    model_version TEXT,
    FOREIGN KEY (record_id) REFERENCES chemical_records(record_id)
);
