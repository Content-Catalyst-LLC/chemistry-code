DROP TABLE IF EXISTS barrier_cases;
DROP TABLE IF EXISTS turnover_experiments;
DROP TABLE IF EXISTS adsorption_cases;
DROP TABLE IF EXISTS enzyme_cases;
DROP TABLE IF EXISTS catalytic_cycle_cases;
DROP TABLE IF EXISTS deactivation_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE barrier_cases (
    case_id TEXT PRIMARY KEY,
    temperature_K REAL NOT NULL,
    delta_Ea_kJ_mol REAL NOT NULL
);

CREATE TABLE turnover_experiments (
    experiment TEXT PRIMARY KEY,
    catalyst_type TEXT NOT NULL,
    product_mol REAL NOT NULL,
    catalyst_mol REAL NOT NULL,
    time_s REAL NOT NULL
);

CREATE TABLE adsorption_cases (
    case_id TEXT PRIMARY KEY,
    pressure REAL NOT NULL,
    K_A REAL NOT NULL,
    K_B REAL NOT NULL,
    k_surface REAL NOT NULL
);

CREATE TABLE enzyme_cases (
    case_id TEXT PRIMARY KEY,
    substrate_mM REAL NOT NULL,
    Vmax_umol_min REAL NOT NULL,
    Km_mM REAL NOT NULL
);

CREATE TABLE catalytic_cycle_cases (
    case_id TEXT PRIMARY KEY,
    k_bind REAL NOT NULL,
    k_release REAL NOT NULL,
    k_product REAL NOT NULL,
    catalyst_total_mol_l REAL NOT NULL,
    substrate_initial_mol_l REAL NOT NULL,
    total_time_s REAL NOT NULL,
    time_step_s REAL NOT NULL
);

CREATE TABLE deactivation_cases (
    case_id TEXT PRIMARY KEY,
    initial_activity REAL NOT NULL,
    decay_constant_per_s REAL NOT NULL,
    total_time_s REAL NOT NULL,
    time_step_s REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO barrier_cases VALUES
('modest_barrier_lowering',298.15,10.0),
('strong_barrier_lowering',298.15,40.0),
('industrial_temperature',600.0,40.0),
('mild_enzyme_like',310.15,25.0);

INSERT INTO turnover_experiments VALUES
('homogeneous_demo','homogeneous',0.050,0.00050,3600),
('enzyme_demo','enzyme',0.00080,0.000002,60),
('heterogeneous_demo','heterogeneous',1.50,0.0050,7200),
('screening_demo','organocatalyst',0.010,0.00010,1800);

INSERT INTO adsorption_cases VALUES
('surface_case_001',0.05,1.5,0.8,0.25),
('surface_case_002',0.10,1.5,0.8,0.25),
('surface_case_003',0.25,1.5,0.8,0.25),
('surface_case_004',0.50,1.5,0.8,0.25),
('surface_case_005',1.00,1.5,0.8,0.25),
('surface_case_006',2.00,1.5,0.8,0.25),
('surface_case_007',5.00,1.5,0.8,0.25),
('surface_case_008',10.00,1.5,0.8,0.25);

INSERT INTO enzyme_cases VALUES
('enzyme_001',0.05,2.0,0.75),
('enzyme_002',0.10,2.0,0.75),
('enzyme_003',0.25,2.0,0.75),
('enzyme_004',0.50,2.0,0.75),
('enzyme_005',1.00,2.0,0.75),
('enzyme_006',2.00,2.0,0.75),
('enzyme_007',5.00,2.0,0.75),
('enzyme_008',10.00,2.0,0.75);

INSERT INTO catalytic_cycle_cases VALUES
('cycle_demo_001',0.80,0.20,0.40,0.010,0.100,60,0.5),
('cycle_demo_002',1.20,0.15,0.60,0.010,0.100,60,0.5),
('cycle_demo_003',0.50,0.30,0.20,0.010,0.100,60,0.5);

INSERT INTO deactivation_cases VALUES
('stable_catalyst',1.0,0.0005,3600,300),
('moderate_deactivation',1.0,0.0020,3600,300),
('rapid_deactivation',1.0,0.0060,3600,300);

INSERT INTO workflow_steps VALUES
(1,'barrier_rate_enhancement','barrier_cases.csv','python/01_barrier_rate_enhancement.py','outputs/tables/barrier_rate_enhancement.csv','Estimate catalytic rate enhancement from activation barrier lowering'),
(2,'turnover_metrics','turnover_experiments.csv','python/02_turnover_metrics.py','outputs/tables/turnover_metrics.csv','Calculate TON TOF and catalytic activity'),
(3,'adsorption_surface_rates','adsorption_cases.csv;enzyme_cases.csv','python/03_adsorption_surface_rates.py','outputs/tables/adsorption_surface_rates.csv','Calculate Langmuir coverage surface rates and Michaelis-Menten rates'),
(4,'catalytic_cycle_deactivation','catalytic_cycle_cases.csv;deactivation_cases.csv','python/04_catalytic_cycle_deactivation.py','outputs/tables/catalytic_cycle_deactivation.csv','Simulate catalytic cycles and deactivation scaffolds'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_catalysis_report.py','outputs/reports/catalysis_report.md','Generate report');
