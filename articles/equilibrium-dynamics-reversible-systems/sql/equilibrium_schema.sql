DROP TABLE IF EXISTS reaction_quotient_cases;
DROP TABLE IF EXISTS simple_equilibrium_cases;
DROP TABLE IF EXISTS reversible_dynamics_cases;
DROP TABLE IF EXISTS vant_hoff_equilibrium;
DROP TABLE IF EXISTS solubility_cases;
DROP TABLE IF EXISTS activity_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE reaction_quotient_cases (
    case_id TEXT PRIMARY KEY,
    reaction TEXT NOT NULL,
    K REAL NOT NULL,
    temperature_K REAL NOT NULL,
    A_mol_l REAL NOT NULL,
    B_mol_l REAL NOT NULL,
    C_mol_l REAL NOT NULL,
    D_mol_l REAL NOT NULL,
    stoich_A REAL NOT NULL,
    stoich_B REAL NOT NULL,
    stoich_C REAL NOT NULL,
    stoich_D REAL NOT NULL
);

CREATE TABLE simple_equilibrium_cases (
    case_id TEXT PRIMARY KEY,
    reaction TEXT NOT NULL,
    K REAL NOT NULL,
    total_concentration_mol_l REAL NOT NULL,
    initial_A_mol_l REAL NOT NULL,
    initial_B_mol_l REAL NOT NULL
);

CREATE TABLE reversible_dynamics_cases (
    case_id TEXT PRIMARY KEY,
    kf_per_min REAL NOT NULL,
    kr_per_min REAL NOT NULL,
    A0_mol_l REAL NOT NULL,
    B0_mol_l REAL NOT NULL,
    total_time_min REAL NOT NULL,
    time_step_min REAL NOT NULL
);

CREATE TABLE vant_hoff_equilibrium (
    reaction TEXT NOT NULL,
    temperature_K REAL NOT NULL,
    K REAL NOT NULL,
    inverse_temperature_K_inv REAL GENERATED ALWAYS AS (1.0 / temperature_K) VIRTUAL,
    ln_K REAL GENERATED ALWAYS AS (LN(K)) VIRTUAL
);

CREATE TABLE solubility_cases (
    case_id TEXT PRIMARY KEY,
    salt TEXT NOT NULL,
    Ksp REAL NOT NULL,
    cation_concentration_mol_l REAL NOT NULL,
    anion_concentration_mol_l REAL NOT NULL,
    cation_power REAL NOT NULL,
    anion_power REAL NOT NULL
);

CREATE TABLE activity_cases (
    case_id TEXT PRIMARY KEY,
    species TEXT NOT NULL,
    concentration_mol_l REAL NOT NULL,
    activity_coefficient REAL NOT NULL,
    standard_concentration_mol_l REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO reaction_quotient_cases VALUES
('reactant_rich','A + B <=> C',12.0,298.15,1.00,1.00,0.20,1.0,1,1,1,0),
('near_equilibrium','A + B <=> C',12.0,298.15,0.30,0.30,1.05,1.0,1,1,1,0),
('product_rich','A + B <=> C',12.0,298.15,0.05,0.05,1.20,1.0,1,1,1,0),
('four_species','A + B <=> C + D',8.0,298.15,0.40,0.60,0.80,1.20,1,1,1,1);

INSERT INTO simple_equilibrium_cases VALUES
('isomerization_001','A <=> B',4.0,1.0,1.0,0.0),
('isomerization_002','A <=> B',0.25,1.0,1.0,0.0),
('isomerization_003','A <=> B',1.0,2.0,2.0,0.0);

INSERT INTO reversible_dynamics_cases VALUES
('dynamic_001',0.20,0.05,1.0,0.0,50,0.25),
('dynamic_002',0.08,0.12,1.0,0.0,80,0.50),
('dynamic_003',0.30,0.10,0.2,0.8,40,0.25);

INSERT INTO vant_hoff_equilibrium (reaction, temperature_K, K) VALUES
('synthetic_equilibrium',290,0.42),
('synthetic_equilibrium',300,0.60),
('synthetic_equilibrium',310,0.83),
('synthetic_equilibrium',320,1.10),
('synthetic_equilibrium',330,1.42),
('exothermic_equilibrium',290,15.0),
('exothermic_equilibrium',300,11.2),
('exothermic_equilibrium',310,8.6),
('exothermic_equilibrium',320,6.7),
('exothermic_equilibrium',330,5.4);

INSERT INTO solubility_cases VALUES
('calcium_carbonate_below','CaCO3',3.3e-9,2.0e-5,1.0e-4,1,1),
('calcium_carbonate_above','CaCO3',3.3e-9,2.0e-4,1.0e-4,1,1),
('silver_chloride_near','AgCl',1.8e-10,1.4e-5,1.3e-5,1,1),
('magnesium_hydroxide','Mg(OH)2',5.6e-12,1.0e-4,2.0e-4,1,2);

INSERT INTO activity_cases VALUES
('ideal_dilute','A',0.010,1.00,1.0),
('moderate_nonideal','A',0.100,0.82,1.0),
('strong_nonideal','A',1.000,0.55,1.0),
('ion_example','Ca2+',0.005,0.42,1.0);

INSERT INTO workflow_steps VALUES
(1,'reaction_quotient_free_energy','reaction_quotient_cases.csv','python/01_reaction_quotient_free_energy.py','outputs/tables/reaction_quotient_free_energy.csv','Calculate Q compare Q to K and compute Delta G'),
(2,'equilibrium_solver','simple_equilibrium_cases.csv','python/02_equilibrium_solver.py','outputs/tables/equilibrium_solver.csv','Solve simple A reversible B equilibrium from total concentration and K'),
(3,'reversible_dynamics','reversible_dynamics_cases.csv','python/03_reversible_dynamics.py','outputs/tables/reversible_dynamics.csv','Simulate reversible first-order approach to equilibrium'),
(4,'vant_hoff_solubility_activity','vant_hoff_equilibrium.csv;solubility_cases.csv;activity_cases.csv','python/04_vant_hoff_solubility_activity.py','outputs/tables/vant_hoff_solubility_activity.csv','Fit van''t Hoff data summarize Ksp and activity scaffolds'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_equilibrium_report.py','outputs/reports/equilibrium_report.md','Generate report');
