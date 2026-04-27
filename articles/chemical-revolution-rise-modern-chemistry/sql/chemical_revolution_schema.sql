DROP TABLE IF EXISTS mass_conservation_examples;
DROP TABLE IF EXISTS oxidation_mass_gain;
DROP TABLE IF EXISTS combustion_stoichiometry;
DROP TABLE IF EXISTS nomenclature_mapping;
DROP TABLE IF EXISTS historical_notes;
DROP TABLE IF EXISTS provenance_artifacts;

CREATE TABLE mass_conservation_examples (
    reaction TEXT PRIMARY KEY,
    reactant_mass_g REAL NOT NULL,
    product_mass_g REAL NOT NULL,
    system_type TEXT NOT NULL
);

CREATE TABLE oxidation_mass_gain (
    metal TEXT PRIMARY KEY,
    metal_mass_g REAL NOT NULL,
    oxygen_mass_g REAL NOT NULL,
    oxide_name TEXT NOT NULL
);

CREATE TABLE combustion_stoichiometry (
    reaction TEXT PRIMARY KEY,
    carbon_moles REAL NOT NULL,
    oxygen_moles_required REAL NOT NULL,
    carbon_dioxide_moles_produced REAL NOT NULL
);

CREATE TABLE nomenclature_mapping (
    older_name TEXT PRIMARY KEY,
    modern_name TEXT NOT NULL,
    conceptual_shift TEXT NOT NULL
);

CREATE TABLE historical_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    note TEXT NOT NULL
);

CREATE TABLE provenance_artifacts (
    artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum_sha256 TEXT,
    notes TEXT
);

INSERT INTO mass_conservation_examples VALUES
('carbon_combustion_closed',44.0,44.0,'closed'),
('magnesium_oxidation_closed',40.3,40.3,'closed'),
('water_formation_closed',36.0,36.0,'closed'),
('apparent_open_combustion',12.0,44.0,'open_environment_includes_oxygen');

INSERT INTO oxidation_mass_gain VALUES
('magnesium',24.305,16.000,'magnesium_oxide'),
('iron',55.845,16.000,'iron_oxide_simplified'),
('copper',63.546,16.000,'copper_oxide_simplified'),
('mercury',200.592,16.000,'mercury_oxide_simplified');

INSERT INTO combustion_stoichiometry VALUES
('carbon_combustion',1.0,1.0,1.0),
('carbon_combustion_half_mole',0.5,0.5,0.5),
('carbon_combustion_two_moles',2.0,2.0,2.0);

INSERT INTO nomenclature_mapping VALUES
('fixed air','carbon dioxide','gas as chemical substance'),
('inflammable air','hydrogen','gas as chemical substance'),
('dephlogisticated air','oxygen','oxygen theory'),
('calx of mercury','mercury oxide','oxide as compound'),
('marine acid','hydrochloric acid','systematic acid naming'),
('vitriolic acid','sulfuric acid','systematic acid naming');

INSERT INTO historical_notes (topic, note) VALUES
('conservation_of_mass','Closed-system mass accounting became central to modern chemistry.'),
('oxygen_theory','Combustion was reinterpreted as combination with oxygen.'),
('nomenclature','Systematic nomenclature helped reorganize chemical knowledge.'),
('historical_caution','The examples use modern formulas to illustrate historical conceptual shifts.');

INSERT INTO provenance_artifacts (artifact_name, artifact_type, relative_path, checksum_sha256, notes) VALUES
('mass_conservation_examples.csv','synthetic_data','data/mass_conservation_examples.csv',NULL,'Synthetic mass-conservation examples'),
('oxidation_mass_gain.csv','synthetic_data','data/oxidation_mass_gain.csv',NULL,'Synthetic oxidation mass-gain examples'),
('combustion_stoichiometry.csv','synthetic_data','data/combustion_stoichiometry.csv',NULL,'Synthetic combustion stoichiometry examples'),
('nomenclature_mapping.csv','synthetic_data','data/nomenclature_mapping.csv',NULL,'Synthetic nomenclature mapping');
