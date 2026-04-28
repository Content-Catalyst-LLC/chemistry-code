DROP TABLE IF EXISTS constants;
DROP TABLE IF EXISTS orbitals;
DROP TABLE IF EXISTS electron_configurations;
DROP TABLE IF EXISTS effective_nuclear_charge;
DROP TABLE IF EXISTS particle_box_examples;
DROP TABLE IF EXISTS hamiltonian_matrices;

CREATE TABLE constants (
    constant TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE orbitals (
    subshell TEXT PRIMARY KEY,
    l INTEGER NOT NULL,
    label TEXT NOT NULL,
    orbital_count INTEGER GENERATED ALWAYS AS (2 * l + 1) VIRTUAL,
    maximum_electrons INTEGER GENERATED ALWAYS AS (2 * (2 * l + 1)) VIRTUAL
);

CREATE TABLE electron_configurations (
    symbol TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    atomic_number INTEGER NOT NULL,
    configuration TEXT NOT NULL,
    valence_shell INTEGER NOT NULL,
    valence_electrons INTEGER NOT NULL,
    block TEXT NOT NULL
);

CREATE TABLE effective_nuclear_charge (
    symbol TEXT PRIMARY KEY,
    atomic_number INTEGER NOT NULL,
    shielding_constant REAL NOT NULL,
    effective_nuclear_charge REAL GENERATED ALWAYS AS (atomic_number - shielding_constant) VIRTUAL
);

CREATE TABLE particle_box_examples (
    system TEXT PRIMARY KEY,
    box_length_nm REAL NOT NULL,
    max_n INTEGER NOT NULL
);

CREATE TABLE hamiltonian_matrices (
    matrix_name TEXT PRIMARY KEY,
    h11 REAL NOT NULL,
    h12 REAL NOT NULL,
    h13 REAL NOT NULL,
    h21 REAL NOT NULL,
    h22 REAL NOT NULL,
    h23 REAL NOT NULL,
    h31 REAL NOT NULL,
    h32 REAL NOT NULL,
    h33 REAL NOT NULL
);

INSERT INTO constants VALUES
('Planck constant','h',6.62607015e-34,'J s'),
('speed of light','c',299792458,'m/s'),
('elementary charge','e',1.602176634e-19,'C'),
('electron mass','m_e',9.1093837139e-31,'kg'),
('hydrogen ground energy','E1',-13.6,'eV');

INSERT INTO orbitals (subshell,l,label) VALUES
('s',0,'spherical'),
('p',1,'directional'),
('d',2,'complex angular'),
('f',3,'high angular complexity');

INSERT INTO electron_configurations VALUES
('H','Hydrogen',1,'1s1',1,1,'s'),
('He','Helium',2,'1s2',1,2,'s'),
('Li','Lithium',3,'1s2 2s1',2,1,'s'),
('Be','Beryllium',4,'1s2 2s2',2,2,'s'),
('B','Boron',5,'1s2 2s2 2p1',2,3,'p'),
('C','Carbon',6,'1s2 2s2 2p2',2,4,'p'),
('N','Nitrogen',7,'1s2 2s2 2p3',2,5,'p'),
('O','Oxygen',8,'1s2 2s2 2p4',2,6,'p'),
('F','Fluorine',9,'1s2 2s2 2p5',2,7,'p'),
('Ne','Neon',10,'1s2 2s2 2p6',2,8,'p'),
('Na','Sodium',11,'[Ne] 3s1',3,1,'s'),
('Mg','Magnesium',12,'[Ne] 3s2',3,2,'s'),
('Cl','Chlorine',17,'[Ne] 3s2 3p5',3,7,'p'),
('Ar','Argon',18,'[Ne] 3s2 3p6',3,8,'p');

INSERT INTO effective_nuclear_charge (symbol,atomic_number,shielding_constant) VALUES
('H',1,0.00),
('He',2,0.30),
('Li',3,1.70),
('Be',4,2.05),
('B',5,2.40),
('C',6,2.75),
('N',7,3.10),
('O',8,3.45),
('F',9,3.80),
('Ne',10,4.15);

INSERT INTO particle_box_examples VALUES
('one_nm_box',1.0,6),
('two_nm_box',2.0,6),
('five_nm_box',5.0,6);

INSERT INTO hamiltonian_matrices VALUES
('three_state_demo',-1.0,-0.2,0.0,-0.2,-0.7,-0.1,0.0,-0.1,-0.4),
('coupled_orbital_demo',-0.9,-0.3,-0.05,-0.3,-0.6,-0.2,-0.05,-0.2,-0.2);
