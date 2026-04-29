DROP TABLE IF EXISTS species;
DROP TABLE IF EXISTS reactions;
DROP TABLE IF EXISTS stoichiometry;
DROP TABLE IF EXISTS network_cases;
DROP TABLE IF EXISTS parallel_cases;
DROP TABLE IF EXISTS sensitivity_cases;
DROP TABLE IF EXISTS fitting_data;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE species (
    species_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    initial_concentration_mol_l REAL NOT NULL
);

CREATE TABLE reactions (
    reaction_id TEXT PRIMARY KEY,
    reaction TEXT NOT NULL,
    rate_constant REAL NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE stoichiometry (
    species_id TEXT NOT NULL,
    reaction_id TEXT NOT NULL,
    coefficient REAL NOT NULL,
    PRIMARY KEY (species_id, reaction_id)
);

CREATE TABLE network_cases (
    case_id TEXT PRIMARY KEY,
    k1_A_to_B REAL NOT NULL,
    k2_B_to_C REAL NOT NULL,
    k3_A_to_D REAL NOT NULL,
    k4_B_to_E REAL NOT NULL,
    A0 REAL NOT NULL,
    B0 REAL NOT NULL,
    C0 REAL NOT NULL,
    D0 REAL NOT NULL,
    E0 REAL NOT NULL,
    total_time REAL NOT NULL,
    time_step REAL NOT NULL
);

CREATE TABLE parallel_cases (
    case_id TEXT PRIMARY KEY,
    k_to_B REAL NOT NULL,
    k_to_C REAL NOT NULL
);

CREATE TABLE sensitivity_cases (
    case_id TEXT PRIMARY KEY,
    base_k1 REAL NOT NULL,
    delta REAL NOT NULL,
    k2 REAL NOT NULL,
    k3 REAL NOT NULL,
    k4 REAL NOT NULL,
    total_time REAL NOT NULL,
    time_step REAL NOT NULL
);

CREATE TABLE fitting_data (
    time REAL NOT NULL,
    A_observed REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO species VALUES
('A','A',1.0),
('B','B',0.0),
('C','C',0.0),
('D','D',0.0),
('E','E',0.0);

INSERT INTO reactions VALUES
('r1','A_to_B',0.20,'A converts to intermediate B'),
('r2','B_to_C',0.08,'B converts to product C'),
('r3','A_to_D',0.05,'A converts to side product D'),
('r4','B_to_E',0.03,'B branches to side product E');

INSERT INTO stoichiometry VALUES
('A','r1',-1),
('B','r1',1),
('C','r1',0),
('D','r1',0),
('E','r1',0),
('A','r2',0),
('B','r2',-1),
('C','r2',1),
('D','r2',0),
('E','r2',0),
('A','r3',-1),
('B','r3',0),
('C','r3',0),
('D','r3',1),
('E','r3',0),
('A','r4',0),
('B','r4',-1),
('C','r4',0),
('D','r4',0),
('E','r4',1);

INSERT INTO network_cases VALUES
('base_network',0.20,0.08,0.05,0.03,1.0,0.0,0.0,0.0,0.0,50,0.25),
('fast_product',0.20,0.20,0.05,0.03,1.0,0.0,0.0,0.0,0.0,50,0.25),
('side_reaction_high',0.20,0.08,0.15,0.10,1.0,0.0,0.0,0.0,0.0,50,0.25);

INSERT INTO parallel_cases VALUES
('B_favored',0.30,0.05),
('C_favored',0.05,0.30),
('balanced',0.15,0.15),
('weak_selectivity',0.18,0.12);

INSERT INTO sensitivity_cases VALUES
('sensitivity_base',0.20,0.01,0.08,0.05,0.03,50,0.25),
('sensitivity_fast',0.30,0.01,0.08,0.05,0.03,50,0.25),
('sensitivity_slow',0.10,0.01,0.08,0.05,0.03,50,0.25);

INSERT INTO fitting_data VALUES
(0,1.000),
(5,0.472),
(10,0.223),
(15,0.105),
(20,0.050),
(25,0.024),
(30,0.011);

INSERT INTO workflow_steps VALUES
(1,'stoichiometric_matrix','species.csv;reactions.csv;stoichiometry.csv','python/01_stoichiometric_matrix.py','outputs/tables/stoichiometric_matrix.csv','Build stoichiometric matrix and metadata tables'),
(2,'network_ode_simulation','network_cases.csv','python/02_network_ode_simulation.py','outputs/tables/network_ode_simulation.csv','Simulate reaction-network ODE trajectories'),
(3,'parallel_branching_selectivity','parallel_cases.csv;network_cases.csv','python/03_parallel_branching_selectivity.py','outputs/tables/parallel_branching_selectivity.csv','Calculate parallel selectivity and branching outcomes'),
(4,'flux_sensitivity_fitting','sensitivity_cases.csv;fitting_data.csv','python/04_flux_sensitivity_fitting.py','outputs/tables/flux_sensitivity_fitting.csv','Calculate flux tables sensitivity and simple parameter fit'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_network_report.py','outputs/reports/reaction_network_report.md','Generate report');
