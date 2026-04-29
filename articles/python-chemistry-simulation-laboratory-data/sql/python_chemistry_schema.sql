DROP TABLE IF EXISTS calibration_standards;
DROP TABLE IF EXISTS unknown_samples;
DROP TABLE IF EXISTS kinetics_timeseries;
DROP TABLE IF EXISTS arrhenius_rates;
DROP TABLE IF EXISTS replicate_measurements;
DROP TABLE IF EXISTS simulation_parameters;
DROP TABLE IF EXISTS lab_metadata;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE calibration_standards (
    standard_id TEXT PRIMARY KEY,
    concentration_mM REAL NOT NULL,
    response REAL NOT NULL,
    replicate INTEGER NOT NULL
);

CREATE TABLE unknown_samples (
    sample_id TEXT NOT NULL,
    response REAL NOT NULL,
    replicate INTEGER NOT NULL
);

CREATE TABLE kinetics_timeseries (
    time_s REAL PRIMARY KEY,
    concentration_mM REAL NOT NULL,
    temperature_K REAL NOT NULL
);

CREATE TABLE arrhenius_rates (
    temperature_K REAL PRIMARY KEY,
    rate_constant_s_inv REAL NOT NULL
);

CREATE TABLE replicate_measurements (
    sample_id TEXT NOT NULL,
    measurement_mM REAL NOT NULL,
    replicate INTEGER NOT NULL,
    method_id TEXT NOT NULL
);

CREATE TABLE simulation_parameters (
    simulation_id TEXT PRIMARY KEY,
    initial_concentration_mM REAL NOT NULL,
    rate_constant_s_inv REAL NOT NULL,
    time_end_s REAL NOT NULL,
    time_step_s REAL NOT NULL
);

CREATE TABLE lab_metadata (
    record_id TEXT PRIMARY KEY,
    method_id TEXT NOT NULL,
    instrument TEXT NOT NULL,
    operator TEXT NOT NULL,
    date TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO calibration_standards VALUES
('blank_1',0.0,0.020,1),
('blank_2',0.0,0.018,2),
('std_1_a',1.0,0.310,1),
('std_1_b',1.0,0.305,2),
('std_2_a',2.0,0.620,1),
('std_2_b',2.0,0.615,2),
('std_4_a',4.0,1.180,1),
('std_4_b',4.0,1.195,2),
('std_6_a',6.0,1.820,1),
('std_6_b',6.0,1.805,2);

INSERT INTO unknown_samples VALUES
('unknown_A',0.950,1),
('unknown_A',0.965,2),
('unknown_A',0.955,3),
('unknown_B',1.420,1),
('unknown_B',1.405,2),
('unknown_B',1.430,3),
('qc_low',0.335,1),
('qc_high',1.745,1);

INSERT INTO kinetics_timeseries VALUES
(0,10.0,298.15),
(20,7.4,298.15),
(40,5.5,298.15),
(60,4.1,298.15),
(80,3.0,298.15),
(100,2.2,298.15);

INSERT INTO arrhenius_rates VALUES
(290,0.010),
(300,0.018),
(310,0.031),
(320,0.052);

INSERT INTO replicate_measurements VALUES
('sample_A',1.02,1,'method_demo'),
('sample_A',1.05,2,'method_demo'),
('sample_A',0.99,3,'method_demo'),
('sample_B',2.10,1,'method_demo'),
('sample_B',2.05,2,'method_demo'),
('sample_B',2.15,3,'method_demo'),
('sample_C',3.95,1,'method_demo'),
('sample_C',4.05,2,'method_demo'),
('sample_C',4.00,3,'method_demo');

INSERT INTO simulation_parameters VALUES
('first_order_demo',10.0,0.015,200,20),
('fast_decay_demo',10.0,0.030,200,20),
('slow_decay_demo',10.0,0.008,200,20);

INSERT INTO lab_metadata VALUES
('meta_001','method_demo','uv_vis_demo','analyst_demo','2026-04-29','synthetic educational calibration workflow'),
('meta_002','kinetics_demo','uv_vis_demo','analyst_demo','2026-04-29','synthetic educational kinetics workflow'),
('meta_003','simulation_demo','python_workflow','analyst_demo','2026-04-29','synthetic educational simulation workflow');

INSERT INTO workflow_steps VALUES
(1,'calibration_curve','calibration_standards.csv;unknown_samples.csv','python/01_calibration_curve.py','outputs/tables/calibration_curve.csv','Fit calibration curve and estimate unknown concentrations'),
(2,'kinetics_analysis','kinetics_timeseries.csv;arrhenius_rates.csv','python/02_kinetics_analysis.py','outputs/tables/kinetics_analysis.csv','Fit first-order kinetics and Arrhenius transform'),
(3,'uncertainty_qc','replicate_measurements.csv;lab_metadata.csv','python/03_uncertainty_qc.py','outputs/tables/uncertainty_qc.csv','Summarize replicates and QC metadata'),
(4,'simulation_workflow','simulation_parameters.csv','python/04_simulation_workflow.py','outputs/tables/simulation_workflow.csv','Generate simple first-order simulation profiles'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_python_chemistry_report.py','outputs/reports/python_chemistry_report.md','Generate report');
