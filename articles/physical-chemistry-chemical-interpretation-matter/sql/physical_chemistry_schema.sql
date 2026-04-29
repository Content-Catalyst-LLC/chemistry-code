DROP TABLE IF EXISTS thermodynamic_cases;
DROP TABLE IF EXISTS arrhenius_cases;
DROP TABLE IF EXISTS boltzmann_states;
DROP TABLE IF EXISTS electrochemistry_cases;
DROP TABLE IF EXISTS diffusion_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE thermodynamic_cases (
    case_id TEXT PRIMARY KEY,
    delta_g_standard_kj_mol REAL NOT NULL,
    temperature_K REAL NOT NULL,
    reaction_quotient REAL NOT NULL
);

CREATE TABLE arrhenius_cases (
    case_id TEXT PRIMARY KEY,
    temperature_K REAL NOT NULL,
    pre_exponential_s_inv REAL NOT NULL,
    activation_energy_kj_mol REAL NOT NULL
);

CREATE TABLE boltzmann_states (
    state_id TEXT PRIMARY KEY,
    energy_J REAL NOT NULL,
    temperature_K REAL NOT NULL
);

CREATE TABLE electrochemistry_cases (
    case_id TEXT PRIMARY KEY,
    E_standard_V REAL NOT NULL,
    electrons_transferred REAL NOT NULL,
    temperature_K REAL NOT NULL,
    reaction_quotient REAL NOT NULL
);

CREATE TABLE diffusion_cases (
    case_id TEXT PRIMARY KEY,
    grid_points INTEGER NOT NULL,
    dx REAL NOT NULL,
    dt REAL NOT NULL,
    diffusion_coefficient REAL NOT NULL,
    steps INTEGER NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO thermodynamic_cases VALUES
('favorable_demo',-20.0,298.15,1.0),
('near_neutral_demo',0.0,298.15,1.0),
('unfavorable_demo',20.0,298.15,1.0),
('composition_shift_demo',-10.0,298.15,100.0),
('temperature_high_demo',-20.0,350.00,10.0);

INSERT INTO arrhenius_cases VALUES
('T280',280.00,1.0e12,75.0),
('T298',298.15,1.0e12,75.0),
('T320',320.00,1.0e12,75.0),
('T350',350.00,1.0e12,75.0),
('T400',400.00,1.0e12,75.0);

INSERT INTO boltzmann_states VALUES
('state_1',0.0,298.15),
('state_2',1.0e-21,298.15),
('state_3',2.5e-21,298.15),
('state_4',5.0e-21,298.15);

INSERT INTO electrochemistry_cases VALUES
('standard_cell',1.10,2,298.15,1.0),
('product_rich',1.10,2,298.15,100.0),
('reactant_rich',1.10,2,298.15,0.01),
('single_electron_case',0.80,1,298.15,10.0);

INSERT INTO diffusion_cases VALUES
('diffusion_demo',21,1.0,0.05,0.5,20),
('slow_diffusion',21,1.0,0.05,0.2,20),
('fast_diffusion',21,1.0,0.05,0.8,20);

INSERT INTO workflow_steps VALUES
(1,'thermodynamics_equilibrium','thermodynamic_cases.csv','python/01_thermodynamics_equilibrium.py','outputs/tables/thermodynamics_equilibrium.csv','Calculate equilibrium constants and nonstandard Gibbs free energy'),
(2,'arrhenius_kinetics','arrhenius_cases.csv','python/02_arrhenius_kinetics.py','outputs/tables/arrhenius_kinetics.csv','Calculate Arrhenius temperature dependence'),
(3,'boltzmann_diffusion','boltzmann_states.csv;diffusion_cases.csv','python/03_boltzmann_diffusion.py','outputs/tables/boltzmann_diffusion.csv','Calculate Boltzmann populations and diffusion profiles'),
(4,'electrochemistry_transport','electrochemistry_cases.csv','python/04_electrochemistry_transport.py','outputs/tables/electrochemistry_transport.csv','Calculate electrochemical free energy and Nernst potentials'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_physical_chemistry_report.py','outputs/reports/physical_chemistry_report.md','Generate report');
