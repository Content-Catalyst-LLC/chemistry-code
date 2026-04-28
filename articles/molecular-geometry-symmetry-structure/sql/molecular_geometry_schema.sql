DROP TABLE IF EXISTS molecular_coordinates;
DROP TABLE IF EXISTS bonds;
DROP TABLE IF EXISTS angle_definitions;
DROP TABLE IF EXISTS conformer_coordinates;
DROP TABLE IF EXISTS vsepr_examples;
DROP TABLE IF EXISTS symmetry_operations;

CREATE TABLE molecular_coordinates (
    molecule TEXT NOT NULL,
    atom TEXT NOT NULL,
    element TEXT NOT NULL,
    mass_u REAL NOT NULL,
    x_angstrom REAL NOT NULL,
    y_angstrom REAL NOT NULL,
    z_angstrom REAL NOT NULL,
    PRIMARY KEY (molecule, atom)
);

CREATE TABLE bonds (
    molecule TEXT NOT NULL,
    atom_i TEXT NOT NULL,
    atom_j TEXT NOT NULL,
    bond_type TEXT NOT NULL
);

CREATE TABLE angle_definitions (
    molecule TEXT NOT NULL,
    atom_a TEXT NOT NULL,
    atom_b TEXT NOT NULL,
    atom_c TEXT NOT NULL,
    angle_name TEXT NOT NULL
);

CREATE TABLE conformer_coordinates (
    conformer TEXT NOT NULL,
    atom TEXT NOT NULL,
    x_angstrom REAL NOT NULL,
    y_angstrom REAL NOT NULL,
    z_angstrom REAL NOT NULL,
    PRIMARY KEY (conformer, atom)
);

CREATE TABLE vsepr_examples (
    molecule TEXT PRIMARY KEY,
    central_atom TEXT NOT NULL,
    bonding_domains INTEGER NOT NULL,
    lone_pair_domains INTEGER NOT NULL,
    electron_domain_geometry TEXT NOT NULL,
    molecular_geometry TEXT NOT NULL,
    approx_point_group TEXT NOT NULL
);

CREATE TABLE symmetry_operations (
    operation_name TEXT PRIMARY KEY,
    operation_type TEXT NOT NULL,
    angle_degrees REAL,
    axis TEXT
);

INSERT INTO molecular_coordinates VALUES
('water','O','O',15.999,0.000,0.000,0.000),
('water','H1','H',1.008,0.958,0.000,0.000),
('water','H2','H',1.008,-0.239,0.927,0.000),
('carbon_dioxide','C','C',12.011,0.000,0.000,0.000),
('carbon_dioxide','O1','O',15.999,1.160,0.000,0.000),
('carbon_dioxide','O2','O',15.999,-1.160,0.000,0.000),
('ammonia','N','N',14.007,0.000,0.000,0.000),
('ammonia','H1','H',1.008,0.940,0.000,-0.310),
('ammonia','H2','H',1.008,-0.470,0.814,-0.310),
('ammonia','H3','H',1.008,-0.470,-0.814,-0.310),
('methane','C','C',12.011,0.000,0.000,0.000),
('methane','H1','H',1.008,0.629,0.629,0.629),
('methane','H2','H',1.008,-0.629,-0.629,0.629),
('methane','H3','H',1.008,-0.629,0.629,-0.629),
('methane','H4','H',1.008,0.629,-0.629,-0.629);

INSERT INTO bonds VALUES
('water','O','H1','single'),
('water','O','H2','single'),
('carbon_dioxide','C','O1','double'),
('carbon_dioxide','C','O2','double'),
('ammonia','N','H1','single'),
('ammonia','N','H2','single'),
('ammonia','N','H3','single'),
('methane','C','H1','single'),
('methane','C','H2','single'),
('methane','C','H3','single'),
('methane','C','H4','single');

INSERT INTO angle_definitions VALUES
('water','H1','O','H2','H-O-H'),
('carbon_dioxide','O1','C','O2','O-C-O'),
('ammonia','H1','N','H2','H-N-H'),
('methane','H1','C','H2','H-C-H');

INSERT INTO conformer_coordinates VALUES
('A','C1',0.0,0.0,0.0),
('A','C2',1.5,0.0,0.0),
('A','C3',2.5,1.0,0.0),
('A','C4',3.5,1.0,0.5),
('B','C1',0.0,0.0,0.0),
('B','C2',1.5,0.0,0.0),
('B','C3',2.4,1.1,0.1),
('B','C4',3.4,1.2,0.7);

INSERT INTO vsepr_examples VALUES
('CO2','C',2,0,'linear','linear','Dinfh'),
('BF3','B',3,0,'trigonal planar','trigonal planar','D3h'),
('CH4','C',4,0,'tetrahedral','tetrahedral','Td'),
('NH3','N',3,1,'tetrahedral','trigonal pyramidal','C3v'),
('H2O','O',2,2,'tetrahedral','bent','C2v'),
('PCl5','P',5,0,'trigonal bipyramidal','trigonal bipyramidal','D3h'),
('SF6','S',6,0,'octahedral','octahedral','Oh');

INSERT INTO symmetry_operations VALUES
('identity','identity',0,'none'),
('c2_z','rotation',180,'z'),
('c3_z','rotation',120,'z'),
('c4_z','rotation',90,'z'),
('mirror_xy','reflection',0,'xy_plane');
