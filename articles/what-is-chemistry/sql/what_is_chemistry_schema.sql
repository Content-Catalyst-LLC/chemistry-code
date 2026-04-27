DROP TABLE IF EXISTS substances;
DROP TABLE IF EXISTS kinetics_examples;
DROP TABLE IF EXISTS beer_lambert_calibration;
DROP TABLE IF EXISTS ph_examples;
DROP TABLE IF EXISTS provenance_artifacts;

CREATE TABLE substances (
    substance TEXT PRIMARY KEY,
    formula TEXT NOT NULL,
    mass_g REAL NOT NULL,
    molar_mass_g_mol REAL NOT NULL,
    volume_l REAL NOT NULL
);

CREATE TABLE kinetics_examples (
    reaction TEXT PRIMARY KEY,
    initial_concentration_mol_l REAL NOT NULL,
    rate_constant_per_min REAL NOT NULL,
    total_time_min INTEGER NOT NULL,
    time_step_min INTEGER NOT NULL
);

CREATE TABLE beer_lambert_calibration (
    concentration_mol_l REAL NOT NULL,
    absorbance REAL NOT NULL
);

CREATE TABLE ph_examples (
    solution TEXT PRIMARY KEY,
    hydrogen_concentration_mol_l REAL NOT NULL
);

CREATE TABLE provenance_artifacts (
    artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum_sha256 TEXT,
    notes TEXT
);

INSERT INTO substances VALUES
('sodium_chloride','NaCl',5.844,58.44,0.500),
('glucose','C6H12O6',9.000,180.156,0.250),
('calcium_carbonate','CaCO3',10.000,100.086,0.750);

INSERT INTO kinetics_examples VALUES
('first_order_demo',1.0,0.15,20,2),
('slow_first_order_demo',1.0,0.05,40,5);

INSERT INTO beer_lambert_calibration VALUES
(0.00,0.000),
(0.02,0.115),
(0.04,0.230),
(0.06,0.348),
(0.08,0.459),
(0.10,0.575);

INSERT INTO ph_examples VALUES
('A',1.0e-2),
('B',1.0e-5),
('C',3.2e-4),
('D',7.5e-8);

INSERT INTO provenance_artifacts (artifact_name, artifact_type, relative_path, checksum_sha256, notes) VALUES
('intro_chemistry_examples.csv','synthetic_data','data/intro_chemistry_examples.csv',NULL,'Synthetic introductory chemistry data'),
('kinetics_examples.csv','synthetic_data','data/kinetics_examples.csv',NULL,'Synthetic first-order kinetics data'),
('beer_lambert_calibration.csv','synthetic_data','data/beer_lambert_calibration.csv',NULL,'Synthetic calibration data'),
('ph_examples.csv','synthetic_data','data/ph_examples.csv',NULL,'Synthetic pH data');
