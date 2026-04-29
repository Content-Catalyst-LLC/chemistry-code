DROP TABLE IF EXISTS orbital_mixing_cases;
DROP TABLE IF EXISTS electron_density_grid;
DROP TABLE IF EXISTS huckel_cases;
DROP TABLE IF EXISTS basis_convergence;
DROP TABLE IF EXISTS spin_state_cases;
DROP TABLE IF EXISTS excited_states;
DROP TABLE IF EXISTS tst_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE orbital_mixing_cases (
    case_id TEXT PRIMARY KEY,
    energy_a REAL NOT NULL,
    energy_b REAL NOT NULL,
    coupling REAL NOT NULL
);

CREATE TABLE electron_density_grid (
    grid_point TEXT PRIMARY KEY,
    x REAL NOT NULL,
    orbital_1 REAL NOT NULL,
    orbital_2 REAL NOT NULL,
    occupancy_1 REAL NOT NULL,
    occupancy_2 REAL NOT NULL
);

CREATE TABLE huckel_cases (
    system TEXT PRIMARY KEY,
    alpha REAL NOT NULL,
    beta REAL NOT NULL,
    sites INTEGER NOT NULL
);

CREATE TABLE basis_convergence (
    case_id TEXT NOT NULL,
    basis TEXT NOT NULL,
    energy_hartree REAL NOT NULL,
    basis_size INTEGER NOT NULL,
    PRIMARY KEY (case_id, basis)
);

CREATE TABLE spin_state_cases (
    complex TEXT NOT NULL,
    spin_state TEXT NOT NULL,
    multiplicity INTEGER NOT NULL,
    relative_energy_kj_mol REAL NOT NULL,
    PRIMARY KEY (complex, spin_state)
);

CREATE TABLE excited_states (
    state TEXT PRIMARY KEY,
    relative_energy_kj_mol REAL NOT NULL,
    oscillator_strength REAL NOT NULL,
    temperature_K REAL NOT NULL
);

CREATE TABLE tst_cases (
    reaction TEXT PRIMARY KEY,
    activation_free_energy_kj_mol REAL NOT NULL,
    temperature_K REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO orbital_mixing_cases VALUES
('symmetric_strong',-10.0,-10.0,-2.0),
('asymmetric_moderate',-10.0,-8.0,-2.0),
('weak_coupling',-10.0,-8.0,-0.5),
('large_gap',-12.0,-6.0,-1.0);

INSERT INTO electron_density_grid VALUES
('p01',-3.0,0.011,0.040,2,0),
('p02',-2.5,0.044,0.090,2,0),
('p03',-2.0,0.135,0.180,2,0),
('p04',-1.5,0.325,0.300,2,0),
('p05',-1.0,0.607,0.400,2,0),
('p06',-0.5,0.882,0.450,2,0),
('p07',0.0,1.000,0.000,2,0),
('p08',0.5,0.882,-0.450,2,0),
('p09',1.0,0.607,-0.400,2,0),
('p10',1.5,0.325,-0.300,2,0),
('p11',2.0,0.135,-0.180,2,0),
('p12',2.5,0.044,-0.090,2,0),
('p13',3.0,0.011,-0.040,2,0);

INSERT INTO huckel_cases VALUES
('ethene_like',0.0,-1.0,2),
('allyl_like',0.0,-1.0,3),
('butadiene_like',0.0,-1.0,4);

INSERT INTO basis_convergence VALUES
('water_demo','minimal',-75.9000,7),
('water_demo','double_zeta',-76.0200,24),
('water_demo','triple_zeta',-76.0550,58),
('water_demo','quadruple_zeta',-76.0640,115),
('methane_demo','minimal',-39.7000,9),
('methane_demo','double_zeta',-39.8200,30),
('methane_demo','triple_zeta',-39.8500,72),
('methane_demo','quadruple_zeta',-39.8580,140);

INSERT INTO spin_state_cases VALUES
('metal_demo','low_spin',1,0.0),
('metal_demo','intermediate_spin',3,18.0),
('metal_demo','high_spin',5,7.0),
('radical_pair_demo','singlet',1,0.0),
('radical_pair_demo','triplet',3,4.5);

INSERT INTO excited_states VALUES
('ground',0.0,0.000,298.15),
('excited_1',25.0,0.120,298.15),
('excited_2',60.0,0.450,298.15),
('excited_3',95.0,0.080,298.15);

INSERT INTO tst_cases VALUES
('reaction_A',40,298.15),
('reaction_B',50,298.15),
('reaction_C',60,298.15),
('reaction_D',70,298.15);

INSERT INTO workflow_steps VALUES
(1,'orbital_mixing','orbital_mixing_cases.csv','python/01_orbital_mixing.py','outputs/tables/orbital_mixing.csv','Calculate two-level orbital mixing eigenvalues and eigenvectors'),
(2,'density_huckel','electron_density_grid.csv;huckel_cases.csv','python/02_density_huckel.py','outputs/tables/density_huckel.csv','Calculate electron density scaffold and Hückel-model energy levels'),
(3,'basis_spin_states','basis_convergence.csv;spin_state_cases.csv','python/03_basis_spin_states.py','outputs/tables/basis_spin_states.csv','Calculate basis convergence and spin-state comparisons'),
(4,'excited_states_tst','excited_states.csv;tst_cases.csv','python/04_excited_states_tst.py','outputs/tables/excited_states_tst.csv','Calculate electronic-state populations and transition-state-theory rates'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_quantum_chemistry_report.py','outputs/reports/quantum_chemistry_report.md','Generate report');
