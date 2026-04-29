DROP TABLE IF EXISTS molecular_descriptors;
DROP TABLE IF EXISTS molecular_graphs;
DROP TABLE IF EXISTS conformer_energies;
DROP TABLE IF EXISTS lennard_jones_cases;
DROP TABLE IF EXISTS fingerprints;
DROP TABLE IF EXISTS reaction_energies;
DROP TABLE IF EXISTS md_toy_initial;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE molecular_descriptors (
    molecule TEXT PRIMARY KEY,
    heavy_atoms INTEGER NOT NULL,
    hetero_atoms INTEGER NOT NULL,
    rings INTEGER NOT NULL,
    h_bond_donors INTEGER NOT NULL,
    h_bond_acceptors INTEGER NOT NULL,
    rotatable_bonds INTEGER NOT NULL,
    formal_charge INTEGER NOT NULL
);

CREATE TABLE molecular_graphs (
    molecule TEXT PRIMARY KEY,
    node_count INTEGER NOT NULL,
    edge_count INTEGER NOT NULL,
    aromatic_edges INTEGER NOT NULL,
    hetero_nodes INTEGER NOT NULL,
    connected_components INTEGER NOT NULL
);

CREATE TABLE conformer_energies (
    molecule TEXT NOT NULL,
    conformer TEXT NOT NULL,
    relative_energy_kj_mol REAL NOT NULL,
    temperature_K REAL NOT NULL,
    PRIMARY KEY (molecule, conformer)
);

CREATE TABLE lennard_jones_cases (
    case_id TEXT PRIMARY KEY,
    distance REAL NOT NULL,
    epsilon REAL NOT NULL,
    sigma REAL NOT NULL
);

CREATE TABLE fingerprints (
    molecule TEXT PRIMARY KEY,
    bit_1 INTEGER NOT NULL,
    bit_2 INTEGER NOT NULL,
    bit_3 INTEGER NOT NULL,
    bit_4 INTEGER NOT NULL,
    bit_5 INTEGER NOT NULL,
    bit_6 INTEGER NOT NULL,
    bit_7 INTEGER NOT NULL,
    bit_8 INTEGER NOT NULL
);

CREATE TABLE reaction_energies (
    reaction TEXT PRIMARY KEY,
    reactant_energy_kj_mol REAL NOT NULL,
    product_energy_kj_mol REAL NOT NULL,
    transition_state_energy_kj_mol REAL NOT NULL
);

CREATE TABLE md_toy_initial (
    particle TEXT PRIMARY KEY,
    position REAL NOT NULL,
    velocity REAL NOT NULL,
    mass REAL NOT NULL,
    force REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO molecular_descriptors VALUES
('water',1,1,0,2,1,0,0),
('ethanol',3,1,0,1,1,1,0),
('benzene',6,0,1,0,0,0,0),
('acetic_acid',4,2,0,1,2,1,0),
('aniline',7,1,1,1,1,1,0),
('pyridine',6,1,1,0,1,0,0);

INSERT INTO molecular_graphs VALUES
('water',1,0,0,1,1),
('ethanol',3,2,0,1,1),
('benzene',6,6,6,0,1),
('acetic_acid',4,3,0,2,1),
('aniline',7,7,6,1,1),
('pyridine',6,6,6,1,1);

INSERT INTO conformer_energies VALUES
('butane_like','anti',0.0,298.15),
('butane_like','gauche_1',3.8,298.15),
('butane_like','gauche_2',3.8,298.15),
('butane_like','eclipsed',16.0,298.15),
('flexible_ligand','conf_1',0.0,298.15),
('flexible_ligand','conf_2',2.5,298.15),
('flexible_ligand','conf_3',5.0,298.15),
('flexible_ligand','conf_4',9.0,298.15);

INSERT INTO lennard_jones_cases VALUES
('r_085',0.85,1.0,1.0),
('r_095',0.95,1.0,1.0),
('r_100',1.00,1.0,1.0),
('r_112',1.12,1.0,1.0),
('r_125',1.25,1.0,1.0),
('r_150',1.50,1.0,1.0),
('r_200',2.00,1.0,1.0),
('r_300',3.00,1.0,1.0);

INSERT INTO fingerprints VALUES
('mol_A',1,0,1,1,0,1,0,1),
('mol_B',1,1,1,0,0,1,0,0),
('mol_C',0,0,1,1,1,0,1,1),
('mol_D',1,0,0,1,0,1,1,0);

INSERT INTO reaction_energies VALUES
('reaction_A',0.0,-25.0,55.0),
('reaction_B',0.0,10.0,80.0),
('reaction_C',0.0,-5.0,35.0),
('catalyzed_A',0.0,-25.0,30.0);

INSERT INTO md_toy_initial VALUES
('p1',0.0,0.00,1.0,0.10),
('p2',1.0,0.05,1.0,-0.05),
('p3',2.0,-0.02,2.0,0.02);

INSERT INTO workflow_steps VALUES
(1,'molecular_descriptors','molecular_descriptors.csv;molecular_graphs.csv','python/01_molecular_descriptors.py','outputs/tables/molecular_descriptors.csv','Calculate descriptor and molecular graph scaffolds'),
(2,'conformer_boltzmann','conformer_energies.csv','python/02_conformer_boltzmann.py','outputs/tables/conformer_boltzmann.csv','Calculate Boltzmann conformer populations'),
(3,'potentials_similarity','lennard_jones_cases.csv;fingerprints.csv','python/03_potentials_similarity.py','outputs/tables/potentials_similarity.csv','Calculate Lennard-Jones energies and Tanimoto similarity'),
(4,'reaction_energy_modeling','reaction_energies.csv;md_toy_initial.csv','python/04_reaction_energy_modeling.py','outputs/tables/reaction_energy_modeling.csv','Calculate reaction energy barriers and toy MD update'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_computational_chemistry_report.py','outputs/reports/computational_chemistry_report.md','Generate report');
