DROP TABLE IF EXISTS molecular_coordinates;
DROP TABLE IF EXISTS bonds;
DROP TABLE IF EXISTS bond_polarity;
DROP TABLE IF EXISTS formal_charge_examples;
DROP TABLE IF EXISTS mo_bond_order_examples;
DROP TABLE IF EXISTS vsepr_examples;

CREATE TABLE molecular_coordinates (
    molecule TEXT NOT NULL,
    atom TEXT NOT NULL,
    x_angstrom REAL NOT NULL,
    y_angstrom REAL NOT NULL,
    z_angstrom REAL NOT NULL,
    partial_charge REAL NOT NULL,
    PRIMARY KEY (molecule, atom)
);

CREATE TABLE bonds (
    molecule TEXT NOT NULL,
    atom_i TEXT NOT NULL,
    atom_j TEXT NOT NULL,
    bond_type TEXT NOT NULL
);

CREATE TABLE bond_polarity (
    bond TEXT PRIMARY KEY,
    atom_a TEXT NOT NULL,
    atom_b TEXT NOT NULL,
    chi_a REAL NOT NULL,
    chi_b REAL NOT NULL,
    delta_chi REAL GENERATED ALWAYS AS (abs(chi_a - chi_b)) VIRTUAL
);

CREATE TABLE formal_charge_examples (
    species TEXT PRIMARY KEY,
    atom TEXT NOT NULL,
    valence_electrons REAL NOT NULL,
    nonbonding_electrons REAL NOT NULL,
    bonding_electrons REAL NOT NULL,
    formal_charge REAL GENERATED ALWAYS AS (
        valence_electrons - nonbonding_electrons - bonding_electrons / 2.0
    ) VIRTUAL
);

CREATE TABLE mo_bond_order_examples (
    molecule TEXT PRIMARY KEY,
    bonding_electrons REAL NOT NULL,
    antibonding_electrons REAL NOT NULL,
    bond_order REAL GENERATED ALWAYS AS (
        (bonding_electrons - antibonding_electrons) / 2.0
    ) VIRTUAL
);

CREATE TABLE vsepr_examples (
    molecule TEXT PRIMARY KEY,
    central_atom TEXT NOT NULL,
    bonding_domains INTEGER NOT NULL,
    lone_pair_domains INTEGER NOT NULL,
    electron_domain_geometry TEXT NOT NULL,
    molecular_geometry TEXT NOT NULL
);

INSERT INTO molecular_coordinates VALUES
('water','O',0.000,0.000,0.000,-0.84),
('water','H1',0.958,0.000,0.000,0.42),
('water','H2',-0.239,0.927,0.000,0.42),
('carbon_dioxide','C',0.000,0.000,0.000,0.70),
('carbon_dioxide','O1',1.160,0.000,0.000,-0.35),
('carbon_dioxide','O2',-1.160,0.000,0.000,-0.35),
('ammonia','N',0.000,0.000,0.000,-0.90),
('ammonia','H1',0.940,0.000,-0.310,0.30),
('ammonia','H2',-0.470,0.814,-0.310,0.30),
('ammonia','H3',-0.470,-0.814,-0.310,0.30);

INSERT INTO bonds VALUES
('water','O','H1','single'),
('water','O','H2','single'),
('carbon_dioxide','C','O1','double'),
('carbon_dioxide','C','O2','double'),
('ammonia','N','H1','single'),
('ammonia','N','H2','single'),
('ammonia','N','H3','single');

INSERT INTO bond_polarity (bond,atom_a,atom_b,chi_a,chi_b) VALUES
('C-H','C','H',2.55,2.20),
('O-H','O','H',3.44,2.20),
('Na-Cl','Na','Cl',0.93,3.16),
('C-O','C','O',2.55,3.44),
('N-H','N','H',3.04,2.20),
('C-C','C','C',2.55,2.55);

INSERT INTO formal_charge_examples (species,atom,valence_electrons,nonbonding_electrons,bonding_electrons) VALUES
('neutral_oxygen_single_bonded','O',6,6,2),
('ammonium_nitrogen','N',5,0,8),
('nitrate_single_bonded_oxygen','O',6,6,2),
('carbon_dioxide_carbon','C',4,0,8);

INSERT INTO mo_bond_order_examples (molecule,bonding_electrons,antibonding_electrons) VALUES
('H2',2,0),
('He2',2,2),
('O2_simplified',10,6),
('N2_simplified',10,4);

INSERT INTO vsepr_examples VALUES
('CO2','C',2,0,'linear','linear'),
('BF3','B',3,0,'trigonal planar','trigonal planar'),
('CH4','C',4,0,'tetrahedral','tetrahedral'),
('NH3','N',3,1,'tetrahedral','trigonal pyramidal'),
('H2O','O',2,2,'tetrahedral','bent'),
('PCl5','P',5,0,'trigonal bipyramidal','trigonal bipyramidal'),
('SF6','S',6,0,'octahedral','octahedral');
