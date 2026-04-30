-- Medicinal chemistry decision analytics schema.
-- Educational only. Not a regulatory, clinical, toxicology, synthesis, or patient-care database.

CREATE TABLE IF NOT EXISTS compounds (
    compound_id TEXT PRIMARY KEY,
    project TEXT NOT NULL,
    scaffold_id TEXT,
    target TEXT,
    target_class TEXT,
    therapeutic_area TEXT,
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
    alert_count INTEGER
);

CREATE TABLE IF NOT EXISTS assay_results (
    assay_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id TEXT NOT NULL,
    assay_type TEXT,
    ic50_nM REAL,
    off_target_ic50_nM REAL,
    assay_qc_score REAL,
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
    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)
);

CREATE TABLE IF NOT EXISTS decision_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    compound_id TEXT NOT NULL,
    pIC50 REAL,
    selectivity_window REAL,
    ligand_efficiency_proxy REAL,
    lipophilic_ligand_efficiency REAL,
    oral_property_score REAL,
    safety_liability_score REAL,
    developability_score REAL,
    multiparameter_optimization_score REAL,
    advancement_recommendation TEXT,
    FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)
);
