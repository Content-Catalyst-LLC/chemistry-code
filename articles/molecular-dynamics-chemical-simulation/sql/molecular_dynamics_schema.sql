DROP TABLE IF EXISTS particles_initial;
DROP TABLE IF EXISTS lennard_jones_cases;
DROP TABLE IF EXISTS coulomb_cases;
DROP TABLE IF EXISTS trajectory_positions;
DROP TABLE IF EXISTS rdf_distances;
DROP TABLE IF EXISTS ensemble_protocols;
DROP TABLE IF EXISTS trajectory_summary;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE particles_initial (
    particle TEXT PRIMARY KEY,
    position REAL NOT NULL,
    velocity REAL NOT NULL,
    mass REAL NOT NULL,
    force REAL NOT NULL
);

CREATE TABLE lennard_jones_cases (
    case_id TEXT PRIMARY KEY,
    distance REAL NOT NULL,
    epsilon REAL NOT NULL,
    sigma REAL NOT NULL
);

CREATE TABLE coulomb_cases (
    case_id TEXT PRIMARY KEY,
    charge_i REAL NOT NULL,
    charge_j REAL NOT NULL,
    distance REAL NOT NULL,
    dielectric REAL NOT NULL
);

CREATE TABLE trajectory_positions (
    time_ps REAL PRIMARY KEY,
    x REAL NOT NULL,
    y REAL NOT NULL,
    z REAL NOT NULL
);

CREATE TABLE rdf_distances (
    pair_id TEXT PRIMARY KEY,
    distance REAL NOT NULL
);

CREATE TABLE ensemble_protocols (
    protocol_id TEXT PRIMARY KEY,
    ensemble TEXT NOT NULL,
    temperature_K REAL NOT NULL,
    pressure_bar TEXT NOT NULL,
    timestep_fs REAL NOT NULL,
    production_ns REAL NOT NULL,
    thermostat TEXT NOT NULL,
    barostat TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE trajectory_summary (
    simulation_id TEXT PRIMARY KEY,
    system TEXT NOT NULL,
    atoms INTEGER NOT NULL,
    solvent TEXT NOT NULL,
    force_field TEXT NOT NULL,
    temperature_K REAL NOT NULL,
    production_ns REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO particles_initial VALUES
('p1',0.0,0.00,1.0,0.10),
('p2',1.0,0.05,1.0,-0.05),
('p3',2.0,-0.02,2.0,0.02),
('p4',3.0,0.01,1.5,-0.03);

INSERT INTO lennard_jones_cases VALUES
('r_085',0.85,1.0,1.0),
('r_095',0.95,1.0,1.0),
('r_100',1.00,1.0,1.0),
('r_112',1.12,1.0,1.0),
('r_125',1.25,1.0,1.0),
('r_150',1.50,1.0,1.0),
('r_200',2.00,1.0,1.0),
('r_300',3.00,1.0,1.0);

INSERT INTO coulomb_cases VALUES
('opposite_close',1,-1,1.0,1.0),
('opposite_screened',1,-1,1.0,78.5),
('same_close',1,1,1.0,1.0),
('weak_pair',0.5,-0.5,2.0,20.0);

INSERT INTO trajectory_positions VALUES
(0,0.0,0.0,0.0),
(1,0.4,0.1,0.2),
(2,0.7,0.3,0.1),
(3,1.1,0.2,0.4),
(4,1.3,0.5,0.6),
(5,1.8,0.6,0.7),
(6,2.1,0.7,1.1),
(7,2.4,0.9,1.2);

INSERT INTO rdf_distances VALUES
('pair_001',0.95),
('pair_002',1.02),
('pair_003',1.08),
('pair_004',1.15),
('pair_005',1.20),
('pair_006',1.85),
('pair_007',1.92),
('pair_008',2.05),
('pair_009',2.10),
('pair_010',2.20),
('pair_011',2.75),
('pair_012',2.90),
('pair_013',3.05),
('pair_014',3.20),
('pair_015',3.30);

INSERT INTO ensemble_protocols VALUES
('nve_demo','NVE',298.15,'NA',1.0,1.0,'none','none','constant energy educational scaffold'),
('nvt_demo','NVT',298.15,'NA',2.0,10.0,'velocity_rescale','none','constant volume educational scaffold'),
('npt_demo','NPT',298.15,'1.0',2.0,20.0,'nose_hoover','parrinello_rahman','constant pressure educational scaffold');

INSERT INTO trajectory_summary VALUES
('sim_water_box','water_box',3000,'explicit','TIP3P_demo',298.15,5),
('sim_polymer','polymer_melt',12000,'none','generic_polymer_demo',450.00,20),
('sim_protein','protein_ligand',52000,'explicit','biomolecular_demo',310.00,100);

INSERT INTO workflow_steps VALUES
(1,'velocity_verlet','particles_initial.csv','python/01_velocity_verlet.py','outputs/tables/velocity_verlet.csv','Calculate simple velocity-Verlet update and kinetic energy'),
(2,'potentials','lennard_jones_cases.csv;coulomb_cases.csv','python/02_potentials.py','outputs/tables/potentials.csv','Calculate Lennard-Jones and Coulomb energy scaffolds'),
(3,'trajectory_analysis','trajectory_positions.csv','python/03_trajectory_analysis.py','outputs/tables/trajectory_analysis.csv','Calculate mean-squared displacement and diffusion estimate'),
(4,'rdf_ensemble_metadata','rdf_distances.csv;ensemble_protocols.csv;trajectory_summary.csv','python/04_rdf_ensemble_metadata.py','outputs/tables/rdf_ensemble_metadata.csv','Calculate RDF histogram and summarize ensemble metadata'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_md_report.py','outputs/reports/molecular_dynamics_report.md','Generate report');
