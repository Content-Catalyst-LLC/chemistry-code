-- Advanced medicinal chemistry provenance schema.
-- Educational only. Not a clinical decision database, patient-treatment tool,
-- dosing model, regulatory submission, toxicology determination, synthesis
-- protocol, controlled-substance design workflow, or substitute for qualified
-- professional medicinal chemistry, pharmacology, toxicology, clinical, legal,
-- or regulatory review.

CREATE TABLE IF NOT EXISTS discovery_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    target TEXT NOT NULL,
    target_class TEXT,
    therapeutic_area TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS compounds (
    compound_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    scaffold_id TEXT,
    molecular_weight REAL,
    clogP REAL,
    tpsa REAL,
    hbd INTEGER,
    hba INTEGER,
    rotatable_bonds INTEGER,
    fsp3 REAL,
    aromatic_rings INTEGER,
    formal_charge INTEGER,
    synthetic_accessibility_score REAL,
    alert_count INTEGER,
    FOREIGN KEY (project_id) REFERENCES discovery_projects(project_id)
);

CREATE TABLE IF NOT EXISTS assay_results (
    assay_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id TEXT NOT NULL,
    assay_type TEXT,
    target TEXT,
    ic50_nM REAL,
    off_target_ic50_nM REAL,
    assay_qc_score REAL,
    method_note TEXT,
    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)
);

CREATE TABLE IF NOT EXISTS admet_results (
    admet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id TEXT NOT NULL,
    hERG_ic50_uM REAL,
    cyp3a4_ic50_uM REAL,
    solubility_uM REAL,
    permeability_10_6_cm_s REAL,
    microsomal_half_life_min REAL,
    plasma_protein_binding_percent REAL,
    clearance_mL_min_kg REAL,
    vd_L_kg REAL,
    method_note TEXT,
    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)
);

CREATE TABLE IF NOT EXISTS medicinal_advanced_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id TEXT NOT NULL,
    pIC50 REAL,
    selectivity_window REAL,
    ligand_efficiency_proxy REAL,
    lipophilic_ligand_efficiency REAL,
    lipinski_violations INTEGER,
    veber_violations INTEGER,
    oral_property_score REAL,
    safety_liability_score REAL,
    developability_score REAL,
    multiparameter_optimization_score REAL,
    mc_advancement_probability REAL,
    advancement_recommendation TEXT,
    model_version TEXT,
    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)
);

CREATE TABLE IF NOT EXISTS medicinal_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)
);
