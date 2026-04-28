DROP TABLE IF EXISTS weak_acid_cases;
DROP TABLE IF EXISTS weak_base_cases;
DROP TABLE IF EXISTS buffer_cases;
DROP TABLE IF EXISTS titration_cases;
DROP TABLE IF EXISTS speciation_cases;
DROP TABLE IF EXISTS polyprotic_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE weak_acid_cases (
    case_id TEXT PRIMARY KEY,
    acid TEXT NOT NULL,
    Ka REAL NOT NULL,
    initial_concentration_mol_l REAL NOT NULL
);

CREATE TABLE weak_base_cases (
    case_id TEXT PRIMARY KEY,
    base TEXT NOT NULL,
    Kb REAL NOT NULL,
    initial_concentration_mol_l REAL NOT NULL
);

CREATE TABLE buffer_cases (
    case_id TEXT PRIMARY KEY,
    buffer TEXT NOT NULL,
    pKa REAL NOT NULL,
    weak_acid_mol_l REAL NOT NULL,
    conjugate_base_mol_l REAL NOT NULL
);

CREATE TABLE titration_cases (
    case_id TEXT PRIMARY KEY,
    titration_type TEXT NOT NULL,
    acid_concentration_mol_l REAL NOT NULL,
    acid_volume_l REAL NOT NULL,
    base_concentration_mol_l REAL NOT NULL,
    Ka REAL
);

CREATE TABLE speciation_cases (
    case_id TEXT PRIMARY KEY,
    acid TEXT NOT NULL,
    pKa REAL NOT NULL,
    pH_min REAL NOT NULL,
    pH_max REAL NOT NULL,
    pH_step REAL NOT NULL
);

CREATE TABLE polyprotic_cases (
    case_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    pKa1 REAL NOT NULL,
    pKa2 REAL NOT NULL,
    pKa3 REAL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO weak_acid_cases VALUES
('weak_acid_001','acetic_acid_like',1.8e-5,0.100),
('weak_acid_002','formic_acid_like',1.8e-4,0.100),
('weak_acid_003','benzoic_acid_like',6.3e-5,0.050),
('weak_acid_004','hypochlorous_acid_like',3.0e-8,0.100);

INSERT INTO weak_base_cases VALUES
('weak_base_001','ammonia_like',1.8e-5,0.100),
('weak_base_002','methylamine_like',4.4e-4,0.050),
('weak_base_003','pyridine_like',1.7e-9,0.100);

INSERT INTO buffer_cases VALUES
('buffer_001','acetate_buffer',4.76,0.100,0.120),
('buffer_002','phosphate_buffer_region',7.21,0.100,0.080),
('buffer_003','ammonium_buffer',9.25,0.100,0.050),
('buffer_004','near_equal_buffer',6.86,0.100,0.100);

INSERT INTO titration_cases VALUES
('strong_acid_strong_base','strong_acid_strong_base',0.100,0.025,0.100,NULL),
('weak_acid_strong_base','weak_acid_strong_base',0.100,0.025,0.100,1.8e-5);

INSERT INTO speciation_cases VALUES
('acetic_acid_like','acetic_acid_like',4.76,0,14,0.5),
('ammonium_like','ammonium_like',9.25,0,14,0.5),
('carbonic_first_step_like','carbonic_first_step_like',6.35,0,14,0.5);

INSERT INTO polyprotic_cases VALUES
('phosphoric_acid_like','phosphoric_acid_like',2.15,7.20,12.35),
('carbonic_acid_like','carbonic_acid_like',6.35,10.33,NULL),
('citric_acid_like','citric_acid_like',3.13,4.76,6.40);

INSERT INTO workflow_steps VALUES
(1,'weak_acid_base_ph','weak_acid_cases.csv;weak_base_cases.csv','python/01_weak_acid_base_ph.py','outputs/tables/weak_acid_base_ph.csv','Calculate weak acid and weak base pH scaffolds'),
(2,'buffer_henderson_hasselbalch','buffer_cases.csv','python/02_buffer_henderson_hasselbalch.py','outputs/tables/buffer_henderson_hasselbalch.csv','Calculate buffer pH using Henderson-Hasselbalch relationship'),
(3,'titration_curves','titration_cases.csv','python/03_titration_curves.py','outputs/tables/titration_curves.csv','Generate strong and weak acid titration curve scaffolds'),
(4,'speciation_polyprotic','speciation_cases.csv;polyprotic_cases.csv','python/04_speciation_polyprotic.py','outputs/tables/speciation_polyprotic.csv','Generate monoprotic and polyprotic speciation scaffolds'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_acid_base_report.py','outputs/reports/acid_base_report.md','Generate report');
