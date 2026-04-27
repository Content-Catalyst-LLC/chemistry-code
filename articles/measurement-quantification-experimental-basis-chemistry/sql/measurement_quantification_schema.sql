DROP TABLE IF EXISTS mass_volume_concentration;
DROP TABLE IF EXISTS calibration_curve;
DROP TABLE IF EXISTS unknown_samples;
DROP TABLE IF EXISTS replicate_measurements;
DROP TABLE IF EXISTS dilution_plan;
DROP TABLE IF EXISTS measurement_metadata;
DROP TABLE IF EXISTS provenance_artifacts;

CREATE TABLE mass_volume_concentration (
    sample TEXT PRIMARY KEY,
    substance TEXT NOT NULL,
    formula TEXT NOT NULL,
    mass_g REAL NOT NULL,
    molar_mass_g_mol REAL NOT NULL,
    volume_l REAL NOT NULL
);

CREATE TABLE calibration_curve (
    standard_id TEXT PRIMARY KEY,
    concentration_mol_l REAL NOT NULL,
    instrument_response REAL NOT NULL
);

CREATE TABLE unknown_samples (
    unknown_id TEXT PRIMARY KEY,
    instrument_response REAL NOT NULL
);

CREATE TABLE replicate_measurements (
    sample TEXT NOT NULL,
    replicate INTEGER NOT NULL,
    measured_mass_g REAL NOT NULL,
    PRIMARY KEY (sample, replicate)
);

CREATE TABLE dilution_plan (
    solution TEXT PRIMARY KEY,
    stock_concentration_mol_l REAL NOT NULL,
    target_concentration_mol_l REAL NOT NULL,
    final_volume_ml REAL NOT NULL
);

CREATE TABLE measurement_metadata (
    record_id INTEGER PRIMARY KEY,
    sample TEXT NOT NULL,
    instrument TEXT NOT NULL,
    method TEXT NOT NULL,
    unit TEXT NOT NULL,
    standard_reference TEXT NOT NULL,
    operator_note TEXT NOT NULL
);

CREATE TABLE provenance_artifacts (
    artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum_sha256 TEXT,
    notes TEXT
);

INSERT INTO mass_volume_concentration VALUES
('S1','sodium_chloride','NaCl',5.844,58.44,0.500),
('S2','glucose','C6H12O6',9.000,180.156,0.250),
('S3','copper_sulfate_pentahydrate','CuSO4.5H2O',2.495,249.685,0.100),
('S4','potassium_nitrate','KNO3',1.011,101.103,0.250);

INSERT INTO calibration_curve VALUES
('blank',0.00,0.003),
('std_1',0.02,0.118),
('std_2',0.04,0.231),
('std_3',0.06,0.351),
('std_4',0.08,0.462),
('std_5',0.10,0.579);

INSERT INTO unknown_samples VALUES
('unknown_A',0.405),
('unknown_B',0.288),
('unknown_C',0.522);

INSERT INTO replicate_measurements VALUES
('standard_check',1,1.0032),
('standard_check',2,1.0028),
('standard_check',3,1.0035),
('standard_check',4,1.0030),
('standard_check',5,1.0029),
('standard_check',6,1.0034);

INSERT INTO dilution_plan VALUES
('A',1.0,0.10,100),
('B',0.5,0.05,250),
('C',2.0,0.25,50),
('D',1.5,0.15,200);

INSERT INTO measurement_metadata VALUES
(1,'S1','balance_A','mass_measurement','g','traceable_mass_set','synthetic_example'),
(2,'S1','volumetric_flask_A','solution_preparation','L','class_A_glassware','synthetic_example'),
(3,'std_1','spectrometer_A','calibration_response','absorbance','synthetic_standard_series','synthetic_example'),
(4,'unknown_A','spectrometer_A','unknown_response','absorbance','synthetic_standard_series','synthetic_example');

INSERT INTO provenance_artifacts (artifact_name, artifact_type, relative_path, checksum_sha256, notes) VALUES
('mass_volume_concentration.csv','synthetic_data','data/mass_volume_concentration.csv',NULL,'Synthetic mass volume concentration data'),
('calibration_curve.csv','synthetic_data','data/calibration_curve.csv',NULL,'Synthetic calibration data'),
('unknown_samples.csv','synthetic_data','data/unknown_samples.csv',NULL,'Synthetic unknown response data'),
('replicate_measurements.csv','synthetic_data','data/replicate_measurements.csv',NULL,'Synthetic replicate measurements'),
('dilution_plan.csv','synthetic_data','data/dilution_plan.csv',NULL,'Synthetic dilution plan');
