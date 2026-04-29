DROP TABLE IF EXISTS molecular_formulas;
DROP TABLE IF EXISTS carbon_hybridization_cases;
DROP TABLE IF EXISTS functional_group_cases;
DROP TABLE IF EXISTS molecular_graph_atoms;
DROP TABLE IF EXISTS molecular_graph_edges;
DROP TABLE IF EXISTS stereochemistry_cases;
DROP TABLE IF EXISTS structure_property_cases;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE molecular_formulas (
    molecule TEXT PRIMARY KEY,
    C INTEGER NOT NULL,
    H INTEGER NOT NULL,
    N INTEGER NOT NULL,
    O INTEGER NOT NULL,
    S INTEGER NOT NULL,
    X INTEGER NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE carbon_hybridization_cases (
    case_id TEXT PRIMARY KEY,
    carbon_type TEXT NOT NULL,
    hybridization TEXT NOT NULL,
    approximate_geometry TEXT NOT NULL,
    approximate_bond_angle_degrees REAL NOT NULL,
    sigma_bonds INTEGER NOT NULL,
    pi_bonds INTEGER NOT NULL
);

CREATE TABLE functional_group_cases (
    molecule TEXT PRIMARY KEY,
    alcohol INTEGER NOT NULL,
    ether INTEGER NOT NULL,
    amine INTEGER NOT NULL,
    alkyl_halide INTEGER NOT NULL,
    alkene INTEGER NOT NULL,
    alkyne INTEGER NOT NULL,
    arene INTEGER NOT NULL,
    aldehyde INTEGER NOT NULL,
    ketone INTEGER NOT NULL,
    carboxylic_acid INTEGER NOT NULL,
    ester INTEGER NOT NULL,
    amide INTEGER NOT NULL,
    nitrile INTEGER NOT NULL,
    thiol INTEGER NOT NULL,
    sulfide INTEGER NOT NULL
);

CREATE TABLE molecular_graph_atoms (
    molecule TEXT NOT NULL,
    atom_id TEXT NOT NULL,
    element TEXT NOT NULL,
    PRIMARY KEY (molecule, atom_id)
);

CREATE TABLE molecular_graph_edges (
    molecule TEXT NOT NULL,
    atom_a TEXT NOT NULL,
    atom_b TEXT NOT NULL,
    bond_order REAL NOT NULL,
    bond_type TEXT NOT NULL
);

CREATE TABLE stereochemistry_cases (
    case_id TEXT PRIMARY KEY,
    molecule TEXT NOT NULL,
    stereocenters INTEGER NOT NULL,
    double_bond_stereo_centers INTEGER NOT NULL,
    chiral INTEGER NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE structure_property_cases (
    molecule TEXT PRIMARY KEY,
    carbon_count INTEGER NOT NULL,
    heteroatom_count INTEGER NOT NULL,
    hydrogen_bond_donors INTEGER NOT NULL,
    hydrogen_bond_acceptors INTEGER NOT NULL,
    ring_count INTEGER NOT NULL,
    aromatic_ring_count INTEGER NOT NULL,
    stereocenter_count INTEGER NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO molecular_formulas VALUES
('hexane',6,14,0,0,0,0,'acyclic alkane-like hydrocarbon'),
('cyclohexane',6,12,0,0,0,0,'cycloalkane-like hydrocarbon'),
('benzene',6,6,0,0,0,0,'aromatic hydrocarbon scaffold'),
('acetic_acid',2,4,0,2,0,0,'carboxylic acid scaffold'),
('pyridine_like',5,5,1,0,0,0,'nitrogen heteroaromatic scaffold'),
('chloroethane',2,5,0,0,0,1,'alkyl halide scaffold'),
('thiophene_like',4,4,0,0,1,0,'sulfur heteroaromatic scaffold');

INSERT INTO carbon_hybridization_cases VALUES
('alkane_carbon','tetrahedral_carbon','sp3','tetrahedral',109.5,4,0),
('alkene_carbon','trigonal_planar_carbon','sp2','trigonal planar',120,3,1),
('alkyne_carbon','linear_carbon','sp','linear',180,2,2),
('carbonyl_carbon','trigonal_planar_carbonyl','sp2','trigonal planar',120,3,1),
('aromatic_carbon','aromatic_sp2_carbon','sp2','trigonal planar',120,3,1);

INSERT INTO functional_group_cases VALUES
('ethanol_like',1,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
('diethyl_ether_like',0,1,0,0,0,0,0,0,0,0,0,0,0,0,0),
('ethylamine_like',0,0,1,0,0,0,0,0,0,0,0,0,0,0,0),
('chloroethane_like',0,0,0,1,0,0,0,0,0,0,0,0,0,0,0),
('acetone_like',0,0,0,0,0,0,0,0,1,0,0,0,0,0,0),
('acetic_acid_like',0,0,0,0,0,0,0,0,0,1,0,0,0,0,0),
('ethyl_acetate_like',0,0,0,0,0,0,0,0,0,0,1,0,0,0,0),
('acetamide_like',0,0,0,0,0,0,0,0,0,0,0,1,0,0,0),
('benzonitrile_like',0,0,0,0,0,0,1,0,0,0,0,0,1,0,0),
('thiol_like',0,0,0,0,0,0,0,0,0,0,0,0,0,1,0);

INSERT INTO molecular_graph_atoms VALUES
('ethanol_skeleton','C1','C'),
('ethanol_skeleton','C2','C'),
('ethanol_skeleton','O1','O'),
('acetone_skeleton','C1','C'),
('acetone_skeleton','C2','C'),
('acetone_skeleton','C3','C'),
('acetone_skeleton','O1','O'),
('benzene_skeleton','C1','C'),
('benzene_skeleton','C2','C'),
('benzene_skeleton','C3','C'),
('benzene_skeleton','C4','C'),
('benzene_skeleton','C5','C'),
('benzene_skeleton','C6','C');

INSERT INTO molecular_graph_edges VALUES
('ethanol_skeleton','C1','C2',1,'single'),
('ethanol_skeleton','C2','O1',1,'single'),
('acetone_skeleton','C1','C2',1,'single'),
('acetone_skeleton','C2','C3',1,'single'),
('acetone_skeleton','C2','O1',2,'double'),
('benzene_skeleton','C1','C2',1.5,'aromatic'),
('benzene_skeleton','C2','C3',1.5,'aromatic'),
('benzene_skeleton','C3','C4',1.5,'aromatic'),
('benzene_skeleton','C4','C5',1.5,'aromatic'),
('benzene_skeleton','C5','C6',1.5,'aromatic'),
('benzene_skeleton','C6','C1',1.5,'aromatic');

INSERT INTO stereochemistry_cases VALUES
('achiral_alkane','butane_like',0,0,0,'no stereocenter in simplified scaffold'),
('single_stereocenter','lactic_acid_like',1,0,1,'one tetrahedral stereocenter scaffold'),
('alkene_stereo','disubstituted_alkene_like',0,1,0,'restricted double-bond geometry scaffold'),
('multiple_stereocenters','sugar_like',4,0,1,'multiple stereocenter scaffold'),
('meso_like','meso_tartaric_like',2,0,0,'internal symmetry scaffold');

INSERT INTO structure_property_cases VALUES
('alkane_like',6,0,0,0,0,0,0),
('alcohol_like',4,1,1,1,0,0,0),
('acid_like',3,2,1,2,0,0,0),
('amine_like',3,1,1,1,0,0,0),
('aromatic_like',6,0,0,0,1,1,0),
('chiral_druglike_scaffold',12,4,1,5,2,1,2),
('polymer_monomer_like',8,2,0,2,1,1,0);

INSERT INTO workflow_steps VALUES
(1,'formula_descriptors','molecular_formulas.csv;carbon_hybridization_cases.csv','python/01_formula_descriptors.py','outputs/tables/formula_descriptors.csv','Calculate formula descriptors DBE and hybridization summary'),
(2,'molecular_graphs','molecular_graph_atoms.csv;molecular_graph_edges.csv','python/02_molecular_graphs.py','outputs/tables/molecular_graphs.csv','Build simplified molecular graph adjacency and graph descriptors'),
(3,'functional_groups_stereochemistry','functional_group_cases.csv;stereochemistry_cases.csv','python/03_functional_groups_stereochemistry.py','outputs/tables/functional_groups_stereochemistry.csv','Summarize functional groups and stereochemistry scaffolds'),
(4,'structure_property_scaffold','structure_property_cases.csv','python/04_structure_property_scaffold.py','outputs/tables/structure_property_scaffold.csv','Generate simple organic structure property descriptors'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_organic_structure_report.py','outputs/reports/organic_structure_report.md','Generate report');
