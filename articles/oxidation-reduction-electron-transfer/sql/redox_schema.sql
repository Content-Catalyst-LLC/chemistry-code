DROP TABLE IF EXISTS cell_potential_cases;
DROP TABLE IF EXISTS nernst_cases;
DROP TABLE IF EXISTS redox_titration_cases;
DROP TABLE IF EXISTS ph_redox_cases;
DROP TABLE IF EXISTS corrosion_pairs;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE cell_potential_cases (
    case_id TEXT PRIMARY KEY,
    cell TEXT NOT NULL,
    E_cathode_V REAL NOT NULL,
    E_anode_V REAL NOT NULL,
    electrons_transferred REAL NOT NULL
);

CREATE TABLE nernst_cases (
    case_id TEXT PRIMARY KEY,
    E_standard_V REAL NOT NULL,
    electrons_transferred REAL NOT NULL,
    temperature_K REAL NOT NULL,
    reaction_quotient REAL NOT NULL
);

CREATE TABLE redox_titration_cases (
    case_id TEXT PRIMARY KEY,
    analyte_moles REAL NOT NULL,
    electrons_donated_per_analyte REAL NOT NULL,
    electrons_accepted_per_titrant REAL NOT NULL,
    titrant_concentration_mol_l REAL NOT NULL
);

CREATE TABLE ph_redox_cases (
    case_id TEXT PRIMARY KEY,
    E_standard_V REAL NOT NULL,
    electrons_transferred REAL NOT NULL,
    protons_transferred REAL NOT NULL,
    temperature_K REAL NOT NULL,
    pH_min REAL NOT NULL,
    pH_max REAL NOT NULL,
    pH_step REAL NOT NULL
);

CREATE TABLE corrosion_pairs (
    case_id TEXT PRIMARY KEY,
    metal_a TEXT NOT NULL,
    E_reduction_a_V REAL NOT NULL,
    metal_b TEXT NOT NULL,
    E_reduction_b_V REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO cell_potential_cases VALUES
('cell_001','zinc_copper_demo',0.34,-0.76,2),
('cell_002','iron_copper_demo',0.34,-0.44,2),
('cell_003','hydrogen_copper_demo',0.34,0.00,2),
('cell_004','silver_zinc_demo',0.80,-0.76,2);

INSERT INTO nernst_cases VALUES
('standard_like',1.10,2,298.15,1.0),
('product_rich',1.10,2,298.15,100.0),
('reactant_rich',1.10,2,298.15,0.01),
('high_temperature',1.10,2,320.00,10.0);

INSERT INTO redox_titration_cases VALUES
('one_to_one',0.0020,1,1,0.100),
('permanganate_like',0.0050,1,5,0.020),
('dichromate_like',0.0060,1,6,0.020),
('iodine_thiosulfate_like',0.0040,1,2,0.050);

INSERT INTO ph_redox_cases VALUES
('oxygen_like',1.23,4,4,298.15,0,14,1),
('manganese_like',1.51,5,8,298.15,0,14,1),
('generic_two_electron',0.80,2,2,298.15,0,14,1);

INSERT INTO corrosion_pairs VALUES
('zinc_copper','Zn2+/Zn',-0.76,'Cu2+/Cu',0.34),
('iron_copper','Fe2+/Fe',-0.44,'Cu2+/Cu',0.34),
('magnesium_iron','Mg2+/Mg',-2.37,'Fe2+/Fe',-0.44),
('aluminum_copper','Al3+/Al',-1.66,'Cu2+/Cu',0.34);

INSERT INTO workflow_steps VALUES
(1,'cell_potential_gibbs','cell_potential_cases.csv','python/01_cell_potential_gibbs.py','outputs/tables/cell_potential_gibbs.csv','Calculate standard cell potential Gibbs free energy and equilibrium constants'),
(2,'nernst_equation','nernst_cases.csv','python/02_nernst_equation.py','outputs/tables/nernst_equation.csv','Calculate redox potentials under nonstandard reaction quotients'),
(3,'redox_titration','redox_titration_cases.csv','python/03_redox_titration.py','outputs/tables/redox_titration.csv','Calculate redox titration electron equivalence'),
(4,'ph_corrosion_redox','ph_redox_cases.csv;corrosion_pairs.csv','python/04_ph_corrosion_redox.py','outputs/tables/ph_corrosion_redox.csv','Generate pH dependent redox and galvanic corrosion scaffolds'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_redox_report.py','outputs/reports/redox_report.md','Generate report');
