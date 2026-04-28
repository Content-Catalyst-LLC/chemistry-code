DROP TABLE IF EXISTS reactions;
DROP TABLE IF EXISTS limiting_reagent_examples;
DROP TABLE IF EXISTS solution_examples;
DROP TABLE IF EXISTS titration_examples;
DROP TABLE IF EXISTS gas_stoichiometry_examples;
DROP TABLE IF EXISTS percent_composition_examples;
DROP TABLE IF EXISTS combustion_analysis_examples;
DROP TABLE IF EXISTS reaction_extent_examples;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE reactions (
    reaction_id TEXT PRIMARY KEY,
    equation TEXT NOT NULL,
    reactant_a TEXT NOT NULL,
    coefficient_a REAL NOT NULL,
    reactant_b TEXT,
    coefficient_b REAL,
    product TEXT NOT NULL,
    coefficient_product REAL NOT NULL,
    product_molar_mass_g_mol REAL NOT NULL
);

CREATE TABLE limiting_reagent_examples (
    case_id TEXT PRIMARY KEY,
    reaction_id TEXT NOT NULL,
    available_a_mol REAL NOT NULL,
    available_b_mol REAL,
    actual_yield_g REAL NOT NULL,
    FOREIGN KEY (reaction_id) REFERENCES reactions(reaction_id)
);

CREATE TABLE solution_examples (
    case_id TEXT PRIMARY KEY,
    calculation_type TEXT NOT NULL,
    stock_concentration_mol_l REAL NOT NULL,
    target_concentration_mol_l REAL NOT NULL,
    target_volume_l REAL NOT NULL
);

CREATE TABLE titration_examples (
    case_id TEXT PRIMARY KEY,
    analyte_name TEXT NOT NULL,
    titrant_name TEXT NOT NULL,
    analyte_coefficient REAL NOT NULL,
    titrant_coefficient REAL NOT NULL,
    titrant_concentration_mol_l REAL NOT NULL,
    titrant_volume_l REAL NOT NULL,
    analyte_volume_l REAL NOT NULL
);

CREATE TABLE gas_stoichiometry_examples (
    case_id TEXT PRIMARY KEY,
    reaction_id TEXT NOT NULL,
    gas_species TEXT NOT NULL,
    pressure_atm REAL NOT NULL,
    volume_l REAL NOT NULL,
    temperature_k REAL NOT NULL,
    coefficient_gas REAL NOT NULL,
    coefficient_target REAL NOT NULL,
    target_species TEXT NOT NULL
);

CREATE TABLE percent_composition_examples (
    case_id TEXT NOT NULL,
    element TEXT NOT NULL,
    percent_mass REAL NOT NULL,
    atomic_mass_g_mol REAL NOT NULL
);

CREATE TABLE combustion_analysis_examples (
    case_id TEXT PRIMARY KEY,
    sample_mass_g REAL NOT NULL,
    co2_mass_g REAL NOT NULL,
    h2o_mass_g REAL NOT NULL
);

CREATE TABLE reaction_extent_examples (
    case_id TEXT NOT NULL,
    species TEXT NOT NULL,
    initial_mol REAL NOT NULL,
    stoichiometric_number REAL NOT NULL,
    extent_mol REAL NOT NULL,
    final_mol REAL GENERATED ALWAYS AS (initial_mol + stoichiometric_number * extent_mol) VIRTUAL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO reactions VALUES
('water_synthesis','2 H2 + O2 -> 2 H2O','H2',2,'O2',1,'H2O',2,18.01528),
('ammonia_synthesis','N2 + 3 H2 -> 2 NH3','N2',1,'H2',3,'NH3',2,17.03052),
('carbon_dioxide_formation','C + O2 -> CO2','C',1,'O2',1,'CO2',1,44.00950),
('calcium_carbonate_decomposition','CaCO3 -> CaO + CO2','CaCO3',1,NULL,0,'CO2',1,44.00950);

INSERT INTO limiting_reagent_examples VALUES
('case_001','water_synthesis',4.00,1.50,45.00),
('case_002','ammonia_synthesis',2.00,5.00,50.00),
('case_003','carbon_dioxide_formation',3.00,2.20,82.00);

INSERT INTO solution_examples VALUES
('dilution_001','dilution',1.000,0.100,0.250),
('dilution_002','dilution',2.000,0.250,0.100),
('dilution_003','dilution',0.500,0.050,0.500);

INSERT INTO titration_examples VALUES
('acid_base_001','HCl','NaOH',1,1,0.1000,0.02340,0.02500),
('diprotic_001','H2SO4','NaOH',1,2,0.1000,0.03000,0.02500),
('redox_001','Fe2+','MnO4-',5,1,0.0200,0.01800,0.02500);

INSERT INTO gas_stoichiometry_examples VALUES
('gas_001','water_synthesis','O2',1.000,2.500,298.15,1,2,'H2O'),
('gas_002','ammonia_synthesis','N2',1.000,5.000,298.15,1,2,'NH3');

INSERT INTO percent_composition_examples VALUES
('glucose_like','C',40.00,12.011),
('glucose_like','H',6.71,1.008),
('glucose_like','O',53.29,15.999),
('hydrocarbon_like','C',85.63,12.011),
('hydrocarbon_like','H',14.37,1.008);

INSERT INTO combustion_analysis_examples VALUES
('combustion_001',1.000,1.466,0.600),
('combustion_002',2.000,5.993,1.636);

INSERT INTO reaction_extent_examples (case_id,species,initial_mol,stoichiometric_number,extent_mol) VALUES
('water_extent','H2',4.00,-2,1.50),
('water_extent','O2',1.50,-1,1.50),
('water_extent','H2O',0.00,2,1.50),
('ammonia_extent','N2',2.00,-1,1.50),
('ammonia_extent','H2',5.00,-3,1.50),
('ammonia_extent','NH3',0.00,2,1.50);

INSERT INTO workflow_steps VALUES
(1,'limiting_reagent_yield','reactions.csv;limiting_reagent_examples.csv','python/01_limiting_reagent_yield.py','outputs/tables/limiting_reagent_yield.csv','Calculate limiting reagent theoretical yield and percent yield'),
(2,'solution_titration_gas','solution_examples.csv;titration_examples.csv;gas_stoichiometry_examples.csv','python/02_solution_titration_gas.py','outputs/tables/solution_titration_gas.csv','Calculate dilution titration and gas stoichiometry examples'),
(3,'empirical_formula_combustion','percent_composition_examples.csv;combustion_analysis_examples.csv','python/03_empirical_formula_combustion.py','outputs/tables/empirical_formula_combustion.csv','Infer empirical formula ratios and combustion analysis scaffold'),
(4,'reaction_extent_balances','reaction_extent_examples.csv','python/04_reaction_extent_balances.py','outputs/tables/reaction_extent_balances.csv','Calculate final amounts from reaction extent'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_stoichiometry_report.py','outputs/reports/stoichiometry_report.md','Generate report');
