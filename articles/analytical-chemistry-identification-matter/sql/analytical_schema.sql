DROP TABLE IF EXISTS calibration_standards;
DROP TABLE IF EXISTS blank_signals;
DROP TABLE IF EXISTS unknown_samples;
DROP TABLE IF EXISTS replicate_measurements;
DROP TABLE IF EXISTS spike_recovery;
DROP TABLE IF EXISTS chromatography_peaks;
DROP TABLE IF EXISTS beer_lambert_cases;
DROP TABLE IF EXISTS spectral_vectors;
DROP TABLE IF EXISTS qc_rules;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE calibration_standards (
    standard_id TEXT PRIMARY KEY,
    concentration_mg_L REAL NOT NULL,
    signal REAL NOT NULL
);

CREATE TABLE blank_signals (
    blank_id TEXT PRIMARY KEY,
    signal REAL NOT NULL
);

CREATE TABLE unknown_samples (
    sample_id TEXT PRIMARY KEY,
    signal REAL NOT NULL,
    dilution_factor REAL NOT NULL
);

CREATE TABLE replicate_measurements (
    sample_id TEXT NOT NULL,
    replicate INTEGER NOT NULL,
    measured_mg_L REAL NOT NULL,
    PRIMARY KEY (sample_id, replicate)
);

CREATE TABLE spike_recovery (
    sample_id TEXT PRIMARY KEY,
    unspiked_mg_L REAL NOT NULL,
    spiked_mg_L REAL NOT NULL,
    spike_added_mg_L REAL NOT NULL
);

CREATE TABLE chromatography_peaks (
    pair TEXT PRIMARY KEY,
    tR_1_min REAL NOT NULL,
    tR_2_min REAL NOT NULL,
    w1_min REAL NOT NULL,
    w2_min REAL NOT NULL
);

CREATE TABLE beer_lambert_cases (
    case_id TEXT PRIMARY KEY,
    absorbance REAL NOT NULL,
    epsilon_L_mol_cm REAL NOT NULL,
    path_length_cm REAL NOT NULL
);

CREATE TABLE spectral_vectors (
    wavelength_index INTEGER PRIMARY KEY,
    reference_A REAL NOT NULL,
    unknown_X REAL NOT NULL,
    reference_B REAL NOT NULL
);

CREATE TABLE qc_rules (
    rule_id TEXT PRIMARY KEY,
    metric TEXT NOT NULL,
    lower_limit REAL NOT NULL,
    upper_limit REAL NOT NULL,
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
('blank_standard',0,0.04),
('std_1',1,0.58),
('std_2',2,1.05),
('std_5',5,2.64),
('std_10',10,5.18),
('std_20',20,10.35);

INSERT INTO blank_signals VALUES
('blank_1',0.035),
('blank_2',0.041),
('blank_3',0.039),
('blank_4',0.044),
('blank_5',0.037),
('blank_6',0.040);

INSERT INTO unknown_samples VALUES
('unknown_001',3.72,1),
('unknown_002',6.05,2),
('unknown_003',0.62,1),
('qc_check_sample',5.10,1);

INSERT INTO replicate_measurements VALUES
('sample_A',1,9.8),
('sample_A',2,10.1),
('sample_A',3,10.0),
('sample_A',4,10.2),
('sample_A',5,9.9),
('sample_B',1,2.95),
('sample_B',2,3.05),
('sample_B',3,3.10),
('sample_B',4,2.98),
('sample_B',5,3.02);

INSERT INTO spike_recovery VALUES
('water_matrix_A',4.0,8.8,5.0),
('soil_extract_B',2.2,6.7,5.0),
('serum_matrix_C',1.5,5.6,4.0);

INSERT INTO chromatography_peaks VALUES
('A_B',3.10,5.20,0.42,0.50),
('B_C',5.20,7.00,0.50,0.55),
('C_D',7.00,8.10,0.55,0.60),
('D_E',8.10,8.70,0.60,0.65);

INSERT INTO beer_lambert_cases VALUES
('case_001',0.625,12500,1.0),
('case_002',0.300,9000,1.0),
('case_003',1.150,15000,0.5);

INSERT INTO spectral_vectors VALUES
(1,0.10,0.11,0.80),
(2,0.30,0.32,0.60),
(3,0.75,0.72,0.35),
(4,1.00,0.97,0.20),
(5,0.65,0.66,0.25),
(6,0.25,0.27,0.50),
(7,0.08,0.09,0.75);

INSERT INTO qc_rules VALUES
('recovery_window','recovery_percent',80,120,'educational spike recovery acceptance window'),
('rsd_window','RSD_percent',0,5,'educational replicate precision acceptance window'),
('calibration_r2_window','calibration_r2',0.995,1.0,'educational linear calibration fit window'),
('resolution_window','chromatographic_resolution',1.5,999,'educational baseline separation hint');

INSERT INTO workflow_steps VALUES
(1,'calibration_lod_loq','calibration_standards.csv;blank_signals.csv;unknown_samples.csv','python/01_calibration_lod_loq.py','outputs/tables/calibration_lod_loq.csv','Calculate calibration slope intercept unknown concentrations LOD and LOQ'),
(2,'precision_recovery_qc','replicate_measurements.csv;spike_recovery.csv;qc_rules.csv','python/02_precision_recovery_qc.py','outputs/tables/precision_recovery_qc.csv','Calculate precision RSD recovery and QC flags'),
(3,'chromatography_spectroscopy','chromatography_peaks.csv;beer_lambert_cases.csv','python/03_chromatography_spectroscopy.py','outputs/tables/chromatography_spectroscopy.csv','Calculate chromatographic resolution and Beer-Lambert concentrations'),
(4,'spectral_matching_reporting','spectral_vectors.csv','python/04_spectral_matching_reporting.py','outputs/tables/spectral_matching_reporting.csv','Calculate simple spectral similarity scores and report-ready summary'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_analytical_report.py','outputs/reports/analytical_report.md','Generate report');
