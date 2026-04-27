DROP TABLE IF EXISTS stoichiometry_examples;
DROP TABLE IF EXISTS ph_examples;
DROP TABLE IF EXISTS kinetics_examples;
DROP TABLE IF EXISTS thermodynamics_examples;
DROP TABLE IF EXISTS molecular_coordinates;
DROP TABLE IF EXISTS matrix_examples;
DROP TABLE IF EXISTS uncertainty_components;
DROP TABLE IF EXISTS molecular_graph_edges;
DROP TABLE IF EXISTS provenance_artifacts;

CREATE TABLE stoichiometry_examples (
    reaction TEXT NOT NULL,
    reactant TEXT NOT NULL,
    reactant_moles REAL NOT NULL,
    coefficient_reactant REAL NOT NULL,
    product TEXT NOT NULL,
    coefficient_product REAL NOT NULL
);

CREATE TABLE ph_examples (
    solution TEXT PRIMARY KEY,
    hydrogen_activity REAL NOT NULL
);

CREATE TABLE kinetics_examples (
    reaction TEXT PRIMARY KEY,
    initial_concentration_mol_l REAL NOT NULL,
    rate_constant_per_min REAL NOT NULL,
    total_time_min INTEGER NOT NULL,
    time_step_min INTEGER NOT NULL
);

CREATE TABLE thermodynamics_examples (
    reaction TEXT PRIMARY KEY,
    delta_g_standard_kj_mol REAL NOT NULL,
    temperature_k REAL NOT NULL
);

CREATE TABLE molecular_coordinates (
    molecule TEXT NOT NULL,
    atom TEXT NOT NULL,
    x_angstrom REAL NOT NULL,
    y_angstrom REAL NOT NULL,
    z_angstrom REAL NOT NULL,
    PRIMARY KEY (molecule, atom)
);

CREATE TABLE matrix_examples (
    matrix_name TEXT PRIMARY KEY,
    a11 REAL NOT NULL,
    a12 REAL NOT NULL,
    a21 REAL NOT NULL,
    a22 REAL NOT NULL
);

CREATE TABLE uncertainty_components (
    component TEXT PRIMARY KEY,
    standard_uncertainty REAL NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE molecular_graph_edges (
    molecule TEXT NOT NULL,
    atom_i TEXT NOT NULL,
    atom_j TEXT NOT NULL,
    bond_order REAL NOT NULL
);

CREATE TABLE provenance_artifacts (
    artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum_sha256 TEXT,
    notes TEXT
);

INSERT INTO stoichiometry_examples VALUES
('water_formation','H2',4.0,2,'H2O',2),
('ammonia_synthesis','N2',1.5,1,'NH3',2),
('carbon_combustion','C',2.0,1,'CO2',1);

INSERT INTO ph_examples VALUES
('acidic_solution',1.0e-3),
('near_neutral_solution',1.0e-7),
('weakly_basic_solution',1.0e-9),
('trace_acid_solution',3.2e-5);

INSERT INTO kinetics_examples VALUES
('first_order_demo',1.0,0.15,20,5),
('slow_first_order_demo',1.0,0.05,40,10);

INSERT INTO thermodynamics_examples VALUES
('A_to_B',-5.0,298.15),
('C_to_D',0.0,298.15),
('E_to_F',12.0,298.15),
('G_to_H',-25.0,310.15);

INSERT INTO molecular_coordinates VALUES
('water','O',0.000,0.000,0.000),
('water','H1',0.958,0.000,0.000),
('water','H2',-0.239,0.927,0.000),
('carbon_dioxide','C',0.000,0.000,0.000),
('carbon_dioxide','O1',1.160,0.000,0.000),
('carbon_dioxide','O2',-1.160,0.000,0.000);

INSERT INTO matrix_examples VALUES
('symmetric_demo',2.0,0.5,0.5,1.0),
('coupled_modes_demo',4.0,1.0,1.0,3.0);

INSERT INTO uncertainty_components VALUES
('balance',0.004,'mg/L'),
('volumetric',0.006,'mg/L'),
('calibration',0.015,'mg/L'),
('repeatability',0.012,'mg/L');

INSERT INTO molecular_graph_edges VALUES
('water','O','H1',1),
('water','O','H2',1),
('carbon_dioxide','C','O1',2),
('carbon_dioxide','C','O2',2);

INSERT INTO provenance_artifacts (artifact_name, artifact_type, relative_path, checksum_sha256, notes) VALUES
('stoichiometry_examples.csv','synthetic_data','data/stoichiometry_examples.csv',NULL,'Synthetic stoichiometry examples'),
('ph_examples.csv','synthetic_data','data/ph_examples.csv',NULL,'Synthetic pH examples'),
('kinetics_examples.csv','synthetic_data','data/kinetics_examples.csv',NULL,'Synthetic kinetics examples'),
('thermodynamics_examples.csv','synthetic_data','data/thermodynamics_examples.csv',NULL,'Synthetic thermodynamics examples'),
('molecular_coordinates.csv','synthetic_data','data/molecular_coordinates.csv',NULL,'Synthetic molecular coordinate examples'),
('matrix_examples.csv','synthetic_data','data/matrix_examples.csv',NULL,'Synthetic linear algebra examples'),
('uncertainty_components.csv','synthetic_data','data/uncertainty_components.csv',NULL,'Synthetic uncertainty components'),
('molecular_graph_edges.csv','synthetic_data','data/molecular_graph_edges.csv',NULL,'Synthetic molecular graph examples');
