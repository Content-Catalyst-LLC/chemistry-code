DROP TABLE IF EXISTS replicate_measurements;
DROP TABLE IF EXISTS calibration_standards;
DROP TABLE IF EXISTS unknown_samples;
DROP TABLE IF EXISTS kinetics_timeseries;
DROP TABLE IF EXISTS arrhenius_rates;
DROP TABLE IF EXISTS experimental_design;
DROP TABLE IF EXISTS qc_samples;
DROP TABLE IF EXISTS lab_metadata;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE replicate_measurements (
    sample_id TEXT NOT NULL,
    analyte TEXT NOT NULL,
    measurement_mM REAL NOT NULL,
    replicate INTEGER NOT NULL,
    method_id TEXT NOT NULL,
    batch_id TEXT NOT NULL
);

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

CREATE TABLE experimental_design (
    run_id TEXT PRIMARY KEY,
    temperature_level TEXT NOT NULL,
    catalyst_loading TEXT NOT NULL,
    solvent TEXT NOT NULL,
    yield_percent REAL NOT NULL
);

CREATE TABLE qc_samples (
    qc_id TEXT PRIMARY KEY,
    expected_mM REAL NOT NULL,
    measured_mM REAL NOT NULL,
    batch_id TEXT NOT NULL,
    control_type TEXT NOT NULL
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

INSERT INTO replicate_measurements VALUES
('sample_A','chloride',1.02,1,'method_demo','batch_1'),
('sample_A','chloride',1.05,2,'method_demo','batch_1'),
('sample_A','chloride',0.99,3,'method_demo','batch_1'),
('sample_B','chloride',2.10,1,'method_demo','batch_1'),
('sample_B','chloride',2.05,2,'method_demo','batch_1'),
('sample_B','chloride',2.15,3,'method_demo','batch_1'),
('sample_C','chloride',3.95,1,'method_demo','batch_1'),
('sample_C','chloride',4.05,2,'method_demo','batch_1'),
('sample_C','chloride',4.00,3,'method_demo','batch_1');

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

INSERT INTO experimental_design VALUES
('r1','low','low','solvent_A',45.2),
('r2','low','high','solvent_A',58.1),
('r3','medium','low','solvent_A',62.4),
('r4','medium','high','solvent_A',75.0),
('r5','high','low','solvent_A',65.5),
('r6','high','high','solvent_A',82.3),
('r7','low','low','solvent_B',41.0),
('r8','low','high','solvent_B',55.2),
('r9','medium','low','solvent_B',60.3),
('r10','medium','high','solvent_B',72.6),
('r11','high','low','solvent_B',63.0),
('r12','high','high','solvent_B',79.5);

INSERT INTO qc_samples VALUES
('qc_001',1.00,1.02,'batch_1','low'),
('qc_002',1.00,0.98,'batch_1','low'),
('qc_003',1.00,1.04,'batch_2','low'),
('qc_004',5.00,5.10,'batch_1','high'),
('qc_005',5.00,4.92,'batch_1','high'),
('qc_006',5.00,5.05,'batch_2','high');

INSERT INTO lab_metadata VALUES
('meta_001','method_demo','uv_vis_demo','analyst_demo','2026-04-29','synthetic educational R statistics workflow'),
('meta_002','kinetics_demo','uv_vis_demo','analyst_demo','2026-04-29','synthetic educational kinetics workflow'),
('meta_003','anova_demo','reaction_screen_demo','analyst_demo','2026-04-29','synthetic educational experimental design workflow');

INSERT INTO workflow_steps VALUES
(1,'replicate_summary','replicate_measurements.csv','r/01_replicate_summary.R','outputs/tables/replicate_summary.csv','Summarize replicate measurements and uncertainty'),
(2,'calibration_curve','calibration_standards.csv;unknown_samples.csv','r/02_calibration_curve.R','outputs/tables/calibration_curve.csv','Fit calibration model and estimate unknowns'),
(3,'kinetics_arrhenius','kinetics_timeseries.csv;arrhenius_rates.csv','r/03_kinetics_arrhenius.R','outputs/tables/kinetics_arrhenius.csv','Fit first-order kinetics and Arrhenius transformation'),
(4,'anova_qc','experimental_design.csv;qc_samples.csv','r/04_anova_qc.R','outputs/tables/anova_qc.csv','Analyze experimental design and quality-control samples'),
(5,'report','multiple outputs','r/05_generate_r_chemistry_report.R','outputs/reports/r_chemistry_report.md','Generate report'),
(6,'provenance','workflow_manifest.csv','python/provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums');
