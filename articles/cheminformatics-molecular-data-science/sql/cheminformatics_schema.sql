DROP TABLE IF EXISTS molecules;
DROP TABLE IF EXISTS descriptors;
DROP TABLE IF EXISTS graphs;
DROP TABLE IF EXISTS fingerprints;
DROP TABLE IF EXISTS assays;
DROP TABLE IF EXISTS property_values;
DROP TABLE IF EXISTS scaffold_splits;
DROP TABLE IF EXISTS query_descriptors;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE molecules (
    molecule_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    smiles_like TEXT NOT NULL,
    scaffold TEXT NOT NULL
);

CREATE TABLE descriptors (
    molecule_id TEXT PRIMARY KEY,
    heavy_atoms INTEGER NOT NULL,
    hetero_atoms INTEGER NOT NULL,
    rings INTEGER NOT NULL,
    h_bond_donors INTEGER NOT NULL,
    h_bond_acceptors INTEGER NOT NULL,
    rotatable_bonds INTEGER NOT NULL,
    formal_charge INTEGER NOT NULL
);

CREATE TABLE graphs (
    molecule_id TEXT PRIMARY KEY,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    aromatic_edges INTEGER NOT NULL,
    hetero_nodes INTEGER NOT NULL,
    connected_components INTEGER NOT NULL
);

CREATE TABLE fingerprints (
    molecule_id TEXT PRIMARY KEY,
    bit_1 INTEGER NOT NULL,
    bit_2 INTEGER NOT NULL,
    bit_3 INTEGER NOT NULL,
    bit_4 INTEGER NOT NULL,
    bit_5 INTEGER NOT NULL,
    bit_6 INTEGER NOT NULL,
    bit_7 INTEGER NOT NULL,
    bit_8 INTEGER NOT NULL,
    bit_9 INTEGER NOT NULL,
    bit_10 INTEGER NOT NULL
);

CREATE TABLE assays (
    compound_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    assay_type TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    relation TEXT NOT NULL
);

CREATE TABLE property_values (
    molecule_id TEXT PRIMARY KEY,
    property_name TEXT NOT NULL,
    value REAL NOT NULL
);

CREATE TABLE scaffold_splits (
    molecule_id TEXT PRIMARY KEY,
    scaffold TEXT NOT NULL,
    split TEXT NOT NULL
);

CREATE TABLE query_descriptors (
    query_id TEXT PRIMARY KEY,
    heavy_atoms INTEGER NOT NULL,
    hetero_atoms INTEGER NOT NULL,
    rings INTEGER NOT NULL,
    h_bond_donors INTEGER NOT NULL,
    h_bond_acceptors INTEGER NOT NULL,
    rotatable_bonds INTEGER NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO molecules VALUES
('M001','ethanol','CCO','aliphatic_alcohol'),
('M002','benzene','c1ccccc1','benzene'),
('M003','acetic_acid','CC(=O)O','carboxylic_acid'),
('M004','aniline','Nc1ccccc1','aniline'),
('M005','pyridine','n1ccccc1','pyridine'),
('M006','phenol','Oc1ccccc1','phenol'),
('M007','toluene','Cc1ccccc1','benzene'),
('M008','ethylamine','CCN','aliphatic_amine');

INSERT INTO descriptors VALUES
('M001',3,1,0,1,1,1,0),
('M002',6,0,1,0,0,0,0),
('M003',4,2,0,1,2,1,0),
('M004',7,1,1,1,1,1,0),
('M005',6,1,1,0,1,0,0),
('M006',7,1,1,1,1,0,0),
('M007',7,0,1,0,0,1,0),
('M008',3,1,0,1,1,1,0);

INSERT INTO graphs VALUES
('M001',3,2,0,1,1),
('M002',6,6,6,0,1),
('M003',4,3,0,2,1),
('M004',7,7,6,1,1),
('M005',6,6,6,1,1),
('M006',7,7,6,1,1),
('M007',7,7,6,0,1),
('M008',3,2,0,1,1);

INSERT INTO fingerprints VALUES
('M001',1,0,1,0,0,1,0,0,1,0),
('M002',0,1,1,1,0,0,1,0,0,1),
('M003',1,0,1,0,1,1,0,0,1,0),
('M004',0,1,1,1,0,1,1,0,0,1),
('M005',0,1,1,1,0,0,1,1,0,1),
('M006',0,1,1,1,1,1,1,0,0,1),
('M007',0,1,1,1,0,0,1,0,1,1),
('M008',1,0,1,0,0,1,0,1,1,0);

INSERT INTO assays VALUES
('M001','T001','biochemical',5000,'nM','='),
('M003','T001','biochemical',1200,'nM','='),
('M004','T001','biochemical',80,'nM','='),
('M005','T002','cellular',250,'nM','='),
('M006','T001','biochemical',50,'nM','='),
('M007','T002','cellular',3500,'nM','='),
('M008','T003','biochemical',900,'nM','=');

INSERT INTO property_values VALUES
('M001','solubility_score',0.85),
('M002','solubility_score',0.20),
('M003','solubility_score',0.92),
('M004','solubility_score',0.45),
('M005','solubility_score',0.55),
('M006','solubility_score',0.50),
('M007','solubility_score',0.22),
('M008','solubility_score',0.80);

INSERT INTO scaffold_splits VALUES
('M001','aliphatic_alcohol','train'),
('M002','benzene','train'),
('M003','carboxylic_acid','train'),
('M004','aniline','train'),
('M005','pyridine','test'),
('M006','phenol','test'),
('M007','benzene','train'),
('M008','aliphatic_amine','test');

INSERT INTO query_descriptors VALUES
('Q001',4,1,0,1,1,1),
('Q002',12,4,2,2,5,6),
('Q003',7,1,1,0,1,0);

INSERT INTO workflow_steps VALUES
(1,'descriptors_graphs','molecules.csv;descriptors.csv;graphs.csv','python/01_descriptors_graphs.py','outputs/tables/descriptors_graphs.csv','Calculate descriptor and molecular graph scaffolds'),
(2,'fingerprints_similarity','fingerprints.csv','python/02_fingerprints_similarity.py','outputs/tables/fingerprints_similarity.csv','Calculate pairwise Tanimoto similarity'),
(3,'assay_standardization','assays.csv','python/03_assay_standardization.py','outputs/tables/assay_standardization.csv','Standardize assay units and calculate pIC50'),
(4,'splits_applicability_modeling','descriptors.csv;property_values.csv;scaffold_splits.csv;query_descriptors.csv','python/04_splits_applicability_modeling.py','outputs/tables/splits_applicability_modeling.csv','Calculate scaffold split summaries applicability distances and simple model outputs'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_cheminformatics_report.py','outputs/reports/cheminformatics_report.md','Generate report');
