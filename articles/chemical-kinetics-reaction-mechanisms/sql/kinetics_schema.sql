DROP TABLE IF EXISTS first_order_data;
DROP TABLE IF EXISTS arrhenius_data;
DROP TABLE IF EXISTS mechanism_parameters;
DROP TABLE IF EXISTS enzyme_kinetics_data;
DROP TABLE IF EXISTS reaction_order_examples;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE first_order_data (
    experiment TEXT NOT NULL,
    time_min REAL NOT NULL,
    concentration_mol_l REAL NOT NULL,
    ln_concentration REAL GENERATED ALWAYS AS (LN(concentration_mol_l)) VIRTUAL
);

CREATE TABLE arrhenius_data (
    reaction TEXT NOT NULL,
    temperature_K REAL NOT NULL,
    rate_constant_s_inv REAL NOT NULL,
    inverse_temperature_K_inv REAL GENERATED ALWAYS AS (1.0 / temperature_K) VIRTUAL,
    ln_k REAL GENERATED ALWAYS AS (LN(rate_constant_s_inv)) VIRTUAL
);

CREATE TABLE mechanism_parameters (
    mechanism TEXT PRIMARY KEY,
    k1_per_min REAL NOT NULL,
    k2_per_min REAL NOT NULL,
    A0_mol_l REAL NOT NULL,
    B0_mol_l REAL NOT NULL,
    C0_mol_l REAL NOT NULL,
    total_time_min REAL NOT NULL,
    time_step_min REAL NOT NULL
);

CREATE TABLE enzyme_kinetics_data (
    experiment TEXT NOT NULL,
    substrate_mM REAL NOT NULL,
    rate_umol_min REAL NOT NULL,
    inverse_substrate REAL GENERATED ALWAYS AS (1.0 / substrate_mM) VIRTUAL,
    inverse_rate REAL GENERATED ALWAYS AS (1.0 / rate_umol_min) VIRTUAL
);

CREATE TABLE reaction_order_examples (
    case_id TEXT PRIMARY KEY,
    "order" INTEGER NOT NULL,
    initial_concentration_mol_l REAL NOT NULL,
    rate_constant REAL NOT NULL,
    total_time REAL NOT NULL,
    time_step REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO first_order_data (experiment,time_min,concentration_mol_l) VALUES
('first_order_demo',0,1.000),
('first_order_demo',5,0.741),
('first_order_demo',10,0.549),
('first_order_demo',15,0.407),
('first_order_demo',20,0.301),
('first_order_demo',25,0.223),
('first_order_demo',30,0.165),
('slow_first_order_demo',0,1.000),
('slow_first_order_demo',10,0.607),
('slow_first_order_demo',20,0.368),
('slow_first_order_demo',30,0.223),
('slow_first_order_demo',40,0.135);

INSERT INTO arrhenius_data (reaction,temperature_K,rate_constant_s_inv) VALUES
('synthetic_decomposition',290,0.0012),
('synthetic_decomposition',300,0.0021),
('synthetic_decomposition',310,0.0037),
('synthetic_decomposition',320,0.0063),
('synthetic_decomposition',330,0.0104),
('surface_reaction',300,0.0008),
('surface_reaction',315,0.0019),
('surface_reaction',330,0.0042),
('surface_reaction',345,0.0085),
('surface_reaction',360,0.0158);

INSERT INTO mechanism_parameters VALUES
('consecutive_A_to_B_to_C',0.16,0.06,1.0,0.0,0.0,50,0.5),
('fast_intermediate_case',0.35,0.30,1.0,0.0,0.0,30,0.25);

INSERT INTO enzyme_kinetics_data (experiment,substrate_mM,rate_umol_min) VALUES
('enzyme_demo',0.10,0.18),
('enzyme_demo',0.25,0.39),
('enzyme_demo',0.50,0.63),
('enzyme_demo',1.00,0.91),
('enzyme_demo',2.00,1.18),
('enzyme_demo',5.00,1.47),
('enzyme_demo',10.00,1.62);

INSERT INTO reaction_order_examples VALUES
('zero_order_example',0,1.0,0.025,30,5),
('first_order_example',1,1.0,0.120,30,5),
('second_order_example',2,1.0,0.180,30,5);

INSERT INTO workflow_steps VALUES
(1,'integrated_rate_laws','first_order_data.csv;reaction_order_examples.csv','python/01_integrated_rate_laws.py','outputs/tables/integrated_rate_laws.csv','Fit first-order data and generate integrated rate-law trajectories'),
(2,'arrhenius_analysis','arrhenius_data.csv','python/02_arrhenius_analysis.py','outputs/tables/arrhenius_analysis.csv','Estimate activation energy and pre-exponential factors'),
(3,'reaction_mechanism_odes','mechanism_parameters.csv','python/03_reaction_mechanism_odes.py','outputs/tables/reaction_mechanism_odes.csv','Simulate consecutive reaction mechanisms'),
(4,'enzyme_kinetics','enzyme_kinetics_data.csv','python/04_enzyme_kinetics.py','outputs/tables/enzyme_kinetics.csv','Estimate Michaelis-Menten parameters from transformed data'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_kinetics_report.py','outputs/reports/chemical_kinetics_report.md','Generate report');
