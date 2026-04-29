DROP TABLE IF EXISTS enzyme_kinetics_cases;
DROP TABLE IF EXISTS binding_cases;
DROP TABLE IF EXISTS sequences;
DROP TABLE IF EXISTS biomolecule_classes;
DROP TABLE IF EXISTS metabolic_flux_cases;
DROP TABLE IF EXISTS stoichiometry;
DROP TABLE IF EXISTS network_edges;
DROP TABLE IF EXISTS energy_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE enzyme_kinetics_cases (
    case_id TEXT PRIMARY KEY,
    substrate_mM REAL NOT NULL,
    Vmax_units REAL NOT NULL,
    Km_mM REAL NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE binding_cases (
    case_id TEXT PRIMARY KEY,
    ligand_uM REAL NOT NULL,
    Kd_uM REAL NOT NULL,
    hill_n REAL NOT NULL
);

CREATE TABLE sequences (
    sequence_id TEXT PRIMARY KEY,
    sequence_type TEXT NOT NULL,
    sequence TEXT NOT NULL
);

CREATE TABLE biomolecule_classes (
    class_id TEXT PRIMARY KEY,
    biomolecule_class TEXT NOT NULL,
    monomer_or_unit TEXT NOT NULL,
    major_functions TEXT NOT NULL,
    polymer_or_assembly TEXT NOT NULL
);

CREATE TABLE metabolic_flux_cases (
    case_id TEXT PRIMARY KEY,
    v1_A_to_B REAL NOT NULL,
    v2_B_to_C REAL NOT NULL,
    v3_C_export REAL NOT NULL
);

CREATE TABLE stoichiometry (
    metabolite TEXT PRIMARY KEY,
    v1_A_to_B REAL NOT NULL,
    v2_B_to_C REAL NOT NULL,
    v3_C_export REAL NOT NULL
);

CREATE TABLE network_edges (
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    interaction_type TEXT NOT NULL,
    weight REAL NOT NULL
);

CREATE TABLE energy_cases (
    case_id TEXT PRIMARY KEY,
    equilibrium_constant REAL NOT NULL,
    temperature_K REAL NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO enzyme_kinetics_cases VALUES
('case_001',0.1,120,3.5,'low substrate scaffold'),
('case_002',0.25,120,3.5,'low substrate scaffold'),
('case_003',0.5,120,3.5,'low substrate scaffold'),
('case_004',1.0,120,3.5,'intermediate substrate scaffold'),
('case_005',2.0,120,3.5,'intermediate substrate scaffold'),
('case_006',5.0,120,3.5,'near saturation scaffold'),
('case_007',10.0,120,3.5,'high substrate scaffold'),
('case_008',25.0,120,3.5,'high substrate scaffold');

INSERT INTO binding_cases VALUES
('L001',0.01,2.0,1.0),
('L002',0.05,2.0,1.0),
('L003',0.10,2.0,1.0),
('L004',0.50,2.0,1.0),
('L005',1.00,2.0,1.0),
('L006',2.00,2.0,1.0),
('L007',5.00,2.0,1.0),
('L008',10.00,2.0,1.0),
('L009',50.00,2.0,1.0),
('H001',0.50,2.0,2.0),
('H002',1.00,2.0,2.0),
('H003',2.00,2.0,2.0),
('H004',5.00,2.0,2.0),
('H005',10.00,2.0,2.0);

INSERT INTO sequences VALUES
('protein_demo','protein','MSTNPKPQRKTKRNTNRRPQDVKFPGG'),
('dna_demo','dna','ATGGCTGCTTACGATCGTACCGTTAAGCTAGCTAA'),
('rna_demo','rna','AUGGCUACGUUACGAUAGCUAGCUAA');

INSERT INTO biomolecule_classes VALUES
('proteins','protein','amino_acid','catalysis_structure_transport_signaling','polymer'),
('nucleic_acids','nucleic_acid','nucleotide','information_storage_expression_regulation','polymer'),
('carbohydrates','carbohydrate','monosaccharide','energy_structure_recognition','polymer_or_oligomer'),
('lipids','lipid','fatty_acid_or_isoprenoid_unit','membranes_energy_signaling','assembly_or_small_molecule'),
('metabolites','metabolite','varied','network_intermediates_regulation_energy','varied'),
('cofactors','cofactor','varied','electron_group_transfer_catalysis','varied');

INSERT INTO metabolic_flux_cases VALUES
('balanced_flux',10,10,10),
('B_accumulates',12,8,8),
('C_accumulates',10,10,6),
('low_input',4,4,4);

INSERT INTO stoichiometry VALUES
('A',-1,0,0),
('B',1,-1,0),
('C',0,1,-1);

INSERT INTO network_edges VALUES
('enzyme_A','metabolite_B','catalyzes',1.0),
('metabolite_B','enzyme_C','activates',0.6),
('metabolite_C','enzyme_A','inhibits',-0.5),
('gene_X','enzyme_A','encodes',1.0),
('signal_Y','gene_X','regulates',0.8),
('cofactor_Z','enzyme_C','cofactor_for',0.7);

INSERT INTO energy_cases VALUES
('favorable_coupled_step',1000,298.15,'equilibrium free energy scaffold'),
('near_equilibrium_step',1,298.15,'equilibrium free energy scaffold'),
('unfavorable_step',0.001,298.15,'equilibrium free energy scaffold');

INSERT INTO workflow_steps VALUES
(1,'enzyme_kinetics','enzyme_kinetics_cases.csv','python/01_enzyme_kinetics.py','outputs/tables/enzyme_kinetics.csv','Calculate Michaelis-Menten velocity table'),
(2,'binding_occupancy','binding_cases.csv','python/02_binding_occupancy.py','outputs/tables/binding_occupancy.csv','Calculate simple and Hill-type binding occupancy'),
(3,'sequence_composition','sequences.csv;biomolecule_classes.csv','python/03_sequence_composition.py','outputs/tables/sequence_composition.csv','Calculate sequence composition and biomolecule class descriptors'),
(4,'metabolic_networks','metabolic_flux_cases.csv;stoichiometry.csv;network_edges.csv;energy_cases.csv','python/04_metabolic_networks.py','outputs/tables/metabolic_networks.csv','Calculate flux balance network summary and biochemical free energy scaffold'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_biochemistry_report.py','outputs/reports/biochemistry_report.md','Generate report');
