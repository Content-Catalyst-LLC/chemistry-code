DROP TABLE IF EXISTS calorimetry_examples;
DROP TABLE IF EXISTS formation_enthalpy_examples;
DROP TABLE IF EXISTS gibbs_examples;
DROP TABLE IF EXISTS vant_hoff_examples;
DROP TABLE IF EXISTS phase_transition_examples;
DROP TABLE IF EXISTS coupled_reaction_examples;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE calorimetry_examples (
    experiment TEXT PRIMARY KEY,
    process TEXT NOT NULL,
    solution_mass_g REAL NOT NULL,
    specific_heat_j_g_k REAL NOT NULL,
    temperature_change_k REAL NOT NULL,
    reaction_amount_mol REAL NOT NULL,
    calorimeter_heat_capacity_j_k REAL NOT NULL
);

CREATE TABLE formation_enthalpy_examples (
    reaction_id TEXT NOT NULL,
    species TEXT NOT NULL,
    coefficient REAL NOT NULL,
    delta_h_f_kj_mol REAL NOT NULL,
    phase TEXT NOT NULL
);

CREATE TABLE gibbs_examples (
    reaction TEXT PRIMARY KEY,
    delta_h_kj_mol REAL NOT NULL,
    delta_s_j_mol_k REAL NOT NULL,
    temperature_k REAL NOT NULL,
    reaction_quotient REAL NOT NULL
);

CREATE TABLE vant_hoff_examples (
    reaction TEXT NOT NULL,
    temperature_k REAL NOT NULL,
    equilibrium_constant REAL NOT NULL
);

CREATE TABLE phase_transition_examples (
    substance TEXT NOT NULL,
    transition TEXT NOT NULL,
    temperature_k REAL NOT NULL,
    delta_h_transition_kj_mol REAL NOT NULL,
    entropy_change_j_mol_k REAL NOT NULL
);

CREATE TABLE coupled_reaction_examples (
    coupling_case TEXT NOT NULL,
    step TEXT NOT NULL,
    delta_g_kj_mol REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO calorimetry_examples VALUES
('neutralization_demo','acid_base_neutralization',100.0,4.184,6.20,0.0500,0.0),
('dissolution_demo','endothermic_dissolution',75.0,4.184,-3.10,0.0250,0.0),
('calorimeter_corrected_demo','exothermic_solution_reaction',120.0,4.184,4.50,0.0400,25.0);

INSERT INTO formation_enthalpy_examples VALUES
('methane_combustion','CH4',-1,-74.8,'g'),
('methane_combustion','O2',-2,0.0,'g'),
('methane_combustion','CO2',1,-393.5,'g'),
('methane_combustion','H2O_l',2,-285.8,'l'),
('carbon_monoxide_combustion','CO',-2,-110.5,'g'),
('carbon_monoxide_combustion','O2',-1,0.0,'g'),
('carbon_monoxide_combustion','CO2',2,-393.5,'g'),
('ammonia_formation','N2',-1,0.0,'g'),
('ammonia_formation','H2',-3,0.0,'g'),
('ammonia_formation','NH3',2,-46.1,'g');

INSERT INTO gibbs_examples VALUES
('exergonic_entropy_supported',20.0,120.0,298.15,1.0),
('enthalpy_driven',-80.0,-100.0,298.15,1.0),
('near_equilibrium',-10.0,-33.5,298.15,1.0),
('nonstandard_shift',-25.0,20.0,298.15,50.0);

INSERT INTO vant_hoff_examples VALUES
('synthetic_equilibrium',290,0.42),
('synthetic_equilibrium',300,0.60),
('synthetic_equilibrium',310,0.83),
('synthetic_equilibrium',320,1.10),
('synthetic_equilibrium',330,1.42);

INSERT INTO phase_transition_examples VALUES
('water','vaporization',373.15,40.65,108.94),
('water','fusion',273.15,6.01,22.00),
('ethanol','vaporization',351.52,38.56,109.69),
('carbon_dioxide','sublimation',194.65,25.23,129.62);

INSERT INTO coupled_reaction_examples VALUES
('biosynthesis_coupling','unfavorable_biosynthesis',18.0),
('biosynthesis_coupling','atp_hydrolysis_like_step',-30.5),
('transport_coupling','unfavorable_transport',12.0),
('transport_coupling','ion_gradient_dissipation',-19.0),
('redox_coupling','unfavorable_reduction',22.0),
('redox_coupling','favorable_oxidation',-35.0);

INSERT INTO workflow_steps VALUES
(1,'calorimetry_enthalpy','calorimetry_examples.csv','python/01_calorimetry_enthalpy.py','outputs/tables/calorimetry_enthalpy.csv','Calculate q solution q reaction and molar reaction enthalpy'),
(2,'hess_law_formation_enthalpy','formation_enthalpy_examples.csv','python/02_hess_law_formation_enthalpy.py','outputs/tables/hess_law_formation_enthalpy.csv','Calculate reaction enthalpies from formation enthalpies'),
(3,'gibbs_equilibrium','gibbs_examples.csv','python/03_gibbs_equilibrium.py','outputs/tables/gibbs_equilibrium.csv','Calculate Gibbs free energy equilibrium constants and nonstandard free energy'),
(4,'vant_hoff_phase_coupling','vant_hoff_examples.csv;phase_transition_examples.csv;coupled_reaction_examples.csv','python/04_vant_hoff_phase_coupling.py','outputs/tables/vant_hoff_phase_coupling.csv','Fit van''t Hoff data summarize phase transitions and coupled reactions'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_thermodynamics_report.py','outputs/reports/chemical_thermodynamics_report.md','Generate report');
