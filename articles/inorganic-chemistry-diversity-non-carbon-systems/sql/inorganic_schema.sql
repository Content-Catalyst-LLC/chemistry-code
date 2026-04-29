DROP TABLE IF EXISTS oxidation_state_cases;
DROP TABLE IF EXISTS coordination_cases;
DROP TABLE IF EXISTS ligand_cases;
DROP TABLE IF EXISTS crystal_field_cases;
DROP TABLE IF EXISTS ionic_solid_cases;
DROP TABLE IF EXISTS perovskite_cases;
DROP TABLE IF EXISTS material_descriptor_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE oxidation_state_cases (
    compound TEXT PRIMARY KEY,
    total_charge REAL NOT NULL,
    known_contribution REAL NOT NULL,
    unknown_atom_count REAL NOT NULL,
    unknown_element TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE coordination_cases (
    complex_id TEXT PRIMARY KEY,
    central_atom TEXT NOT NULL,
    formal_oxidation_state REAL NOT NULL,
    coordination_number INTEGER NOT NULL,
    ligand_count INTEGER NOT NULL,
    geometry TEXT NOT NULL,
    charge REAL NOT NULL
);

CREATE TABLE ligand_cases (
    ligand TEXT PRIMARY KEY,
    charge REAL NOT NULL,
    donor_atoms TEXT NOT NULL,
    denticity INTEGER NOT NULL,
    field_strength_hint TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE crystal_field_cases (
    case_id TEXT PRIMARY KEY,
    geometry TEXT NOT NULL,
    d_electron_count INTEGER NOT NULL,
    t2g_electrons INTEGER NOT NULL,
    eg_electrons INTEGER NOT NULL,
    unpaired_electrons INTEGER NOT NULL,
    delta_o_units REAL NOT NULL
);

CREATE TABLE ionic_solid_cases (
    compound TEXT PRIMARY KEY,
    cation_charge REAL NOT NULL,
    anion_charge REAL NOT NULL,
    ionic_separation_relative REAL NOT NULL,
    structure_type_hint TEXT NOT NULL
);

CREATE TABLE perovskite_cases (
    material TEXT PRIMARY KEY,
    r_A REAL NOT NULL,
    r_B REAL NOT NULL,
    r_X REAL NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE material_descriptor_cases (
    material TEXT PRIMARY KEY,
    metal_count INTEGER NOT NULL,
    nonmetal_count INTEGER NOT NULL,
    oxygen_count INTEGER NOT NULL,
    transition_metal_present INTEGER NOT NULL,
    halide_present INTEGER NOT NULL,
    formal_average_metal_oxidation_state REAL NOT NULL,
    structure_dimensionality_hint TEXT NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO oxidation_state_cases VALUES
('NaCl',0,-1,1,'Na','sodium chloride charge-balance scaffold'),
('MgO',0,-2,1,'Mg','magnesium oxide charge-balance scaffold'),
('Fe2O3',0,-6,2,'Fe','iron oxide oxidation-state scaffold'),
('KMnO4',0,-7,1,'Mn','permanganate oxidation-state scaffold'),
('SO4_2_minus',-2,-8,1,'S','sulfate oxidation-state scaffold'),
('Cr2O7_2_minus',-2,-14,2,'Cr','dichromate oxidation-state scaffold'),
('NH4_plus',1,4,1,'N','ammonium oxidation-state scaffold');

INSERT INTO coordination_cases VALUES
('hexaaqua_metal_like','M',2,6,6,'octahedral',2),
('tetraammine_metal_like','M',2,4,4,'tetrahedral_or_square_planar',2),
('square_planar_metal_like','M',2,4,4,'square_planar',0),
('octahedral_low_spin_like','M',3,6,6,'octahedral',3),
('linear_d10_like','M',1,2,2,'linear',1);

INSERT INTO ligand_cases VALUES
('water',0,'O',1,'weak_to_intermediate','neutral oxygen donor scaffold'),
('ammonia',0,'N',1,'intermediate','neutral nitrogen donor scaffold'),
('chloride',-1,'Cl',1,'weak','anionic halide donor scaffold'),
('cyanide',-1,'C',1,'strong','pi-acceptor ligand scaffold'),
('carbon_monoxide',0,'C',1,'strong','neutral pi-acceptor ligand scaffold'),
('ethylenediamine',0,'N;N',2,'intermediate','bidentate chelating ligand scaffold'),
('hydroxide',-1,'O',1,'weak_to_intermediate','anionic oxygen donor scaffold');

INSERT INTO crystal_field_cases VALUES
('octahedral_d3','octahedral',3,3,0,3,1.0),
('octahedral_high_spin_d5','octahedral',5,3,2,5,1.0),
('octahedral_low_spin_d6','octahedral',6,6,0,0,1.0),
('octahedral_high_spin_d6','octahedral',6,4,2,4,1.0),
('octahedral_d8','octahedral',8,6,2,2,1.0);

INSERT INTO ionic_solid_cases VALUES
('NaCl',1,-1,1.00,'rock_salt_like'),
('MgO',2,-2,0.90,'rock_salt_like'),
('CaF2',2,-1,1.10,'fluorite_like'),
('Al2O3',3,-2,0.85,'corundum_like'),
('LiF',1,-1,0.75,'rock_salt_like');

INSERT INTO perovskite_cases VALUES
('case_A',1.60,0.60,1.40,'synthetic radius scaffold'),
('case_B',1.35,0.65,1.40,'synthetic radius scaffold'),
('case_C',1.80,0.58,1.40,'synthetic radius scaffold'),
('case_D',1.20,0.75,1.35,'synthetic radius scaffold');

INSERT INTO material_descriptor_cases VALUES
('oxide_catalyst_like',2,3,3,1,0,3,'extended_solid'),
('halide_perovskite_like',1,4,0,0,1,2,'extended_solid'),
('phosphate_mineral_like',3,8,8,0,0,2,'extended_solid'),
('coordination_complex_like',1,6,0,1,0,2,'discrete_complex'),
('mixed_metal_oxide_like',3,4,4,1,0,2.67,'extended_solid');

INSERT INTO workflow_steps VALUES
(1,'oxidation_states','oxidation_state_cases.csv','python/01_oxidation_states.py','outputs/tables/oxidation_states.csv','Calculate unknown oxidation states from charge balance'),
(2,'coordination_ligands','coordination_cases.csv;ligand_cases.csv','python/02_coordination_ligands.py','outputs/tables/coordination_ligands.csv','Summarize coordination complexes and ligand descriptors'),
(3,'crystal_field_magnetism','crystal_field_cases.csv','python/03_crystal_field_magnetism.py','outputs/tables/crystal_field_magnetism.csv','Calculate CFSE and spin-only magnetic moment scaffolds'),
(4,'ionic_materials_descriptors','ionic_solid_cases.csv;perovskite_cases.csv;material_descriptor_cases.csv','python/04_ionic_materials_descriptors.py','outputs/tables/ionic_materials_descriptors.csv','Generate ionic solid perovskite and materials descriptors'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_inorganic_report.py','outputs/reports/inorganic_report.md','Generate report');
