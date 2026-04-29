DROP TABLE IF EXISTS dose_response_cases;
DROP TABLE IF EXISTS occupancy_cases;
DROP TABLE IF EXISTS target_engagement_cases;
DROP TABLE IF EXISTS probe_quality_cases;
DROP TABLE IF EXISTS chemoproteomics_competition;
DROP TABLE IF EXISTS selectivity_cases;
DROP TABLE IF EXISTS perturbation_features;
DROP TABLE IF EXISTS network_edges;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE dose_response_cases (
    case_id TEXT PRIMARY KEY,
    compound_uM REAL NOT NULL,
    EC50_uM REAL NOT NULL,
    hill_slope REAL NOT NULL,
    bottom REAL NOT NULL,
    top REAL NOT NULL
);

CREATE TABLE occupancy_cases (
    case_id TEXT PRIMARY KEY,
    ligand_uM REAL NOT NULL,
    Kd_uM REAL NOT NULL
);

CREATE TABLE target_engagement_cases (
    condition TEXT PRIMARY KEY,
    signal_control REAL NOT NULL,
    signal_treated REAL NOT NULL,
    signal_max REAL NOT NULL,
    compound_uM REAL NOT NULL
);

CREATE TABLE probe_quality_cases (
    probe TEXT PRIMARY KEY,
    target_potency_nM REAL NOT NULL,
    off_target_potency_nM REAL NOT NULL,
    cellular_target_engagement REAL NOT NULL,
    inactive_control_available INTEGER NOT NULL,
    solubility_flag INTEGER NOT NULL,
    viability_flag INTEGER NOT NULL
);

CREATE TABLE chemoproteomics_competition (
    protein TEXT PRIMARY KEY,
    control_intensity REAL NOT NULL,
    treated_intensity REAL NOT NULL,
    competition_intensity REAL NOT NULL,
    known_target INTEGER NOT NULL
);

CREATE TABLE selectivity_cases (
    compound TEXT NOT NULL,
    target TEXT NOT NULL,
    activity_nM REAL NOT NULL,
    target_class TEXT NOT NULL
);

CREATE TABLE perturbation_features (
    feature TEXT PRIMARY KEY,
    control REAL NOT NULL,
    treated REAL NOT NULL
);

CREATE TABLE network_edges (
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    interaction_type TEXT NOT NULL,
    weight REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO dose_response_cases VALUES
('D001',0.001,1.5,1.2,0.05,1.00),
('D002',0.010,1.5,1.2,0.05,1.00),
('D003',0.030,1.5,1.2,0.05,1.00),
('D004',0.100,1.5,1.2,0.05,1.00),
('D005',0.300,1.5,1.2,0.05,1.00),
('D006',1.000,1.5,1.2,0.05,1.00),
('D007',3.000,1.5,1.2,0.05,1.00),
('D008',10.000,1.5,1.2,0.05,1.00),
('D009',30.000,1.5,1.2,0.05,1.00);

INSERT INTO occupancy_cases VALUES
('O001',0.01,2.0),
('O002',0.05,2.0),
('O003',0.10,2.0),
('O004',0.50,2.0),
('O005',1.00,2.0),
('O006',2.00,2.0),
('O007',5.00,2.0),
('O008',10.00,2.0),
('O009',50.00,2.0);

INSERT INTO target_engagement_cases VALUES
('low_dose',100,82,20,0.1),
('mid_dose',100,55,20,1.0),
('high_dose',100,22,20,10.0),
('inactive_control',100,97,20,10.0);

INSERT INTO probe_quality_cases VALUES
('probe_A',25,5000,0.90,1,1,1),
('probe_B',500,2000,0.55,0,1,1),
('probe_C',50,250,0.80,1,1,0),
('probe_D',10,10000,0.92,1,0,1);

INSERT INTO chemoproteomics_competition VALUES
('kinase_A',1000,220,850,1),
('enzyme_B',800,760,770,0),
('reader_C',1200,500,1100,1),
('protease_D',600,580,590,0),
('transporter_E',900,300,420,0);

INSERT INTO selectivity_cases VALUES
('compound_A','target_main',20,'primary'),
('compound_A','off_target_1',3000,'off_target'),
('compound_A','off_target_2',5000,'off_target'),
('compound_B','target_main',200,'primary'),
('compound_B','off_target_1',600,'off_target'),
('compound_B','off_target_2',800,'off_target');

INSERT INTO perturbation_features VALUES
('pathway_A',1.0,1.8),
('pathway_B',1.0,0.6),
('pathway_C',1.0,1.2),
('pathway_D',1.0,0.4),
('pathway_E',1.0,1.1);

INSERT INTO network_edges VALUES
('compound_X','target_A','binds',1.0),
('target_A','pathway_A','inhibits',-0.8),
('pathway_A','phenotype_1','drives',0.7),
('target_A','pathway_B','activates',0.4),
('pathway_B','phenotype_2','suppresses',-0.5),
('compound_X','off_target_C','weak_binds',0.2),
('off_target_C','pathway_D','perturbs',0.3);

INSERT INTO workflow_steps VALUES
(1,'dose_response','dose_response_cases.csv;occupancy_cases.csv','python/01_dose_response.py','outputs/tables/dose_response.csv','Calculate dose-response and occupancy scaffolds'),
(2,'target_engagement_probe_quality','target_engagement_cases.csv;probe_quality_cases.csv','python/02_target_engagement_probe_quality.py','outputs/tables/target_engagement_probe_quality.csv','Calculate target engagement and probe quality metrics'),
(3,'chemoproteomics_selectivity','chemoproteomics_competition.csv;selectivity_cases.csv','python/03_chemoproteomics_selectivity.py','outputs/tables/chemoproteomics_selectivity.csv','Calculate chemoproteomic competition and selectivity summaries'),
(4,'perturbation_networks','perturbation_features.csv;network_edges.csv','python/04_perturbation_networks.py','outputs/tables/perturbation_networks.csv','Calculate perturbation-vector and network summaries'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_chemical_biology_report.py','outputs/reports/chemical_biology_report.md','Generate report');
