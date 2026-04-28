DROP TABLE IF EXISTS elements;
DROP TABLE IF EXISTS isotopes;
DROP TABLE IF EXISTS classification_rules;

CREATE TABLE elements (
    symbol TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    atomic_number INTEGER NOT NULL,
    "group" INTEGER,
    period INTEGER NOT NULL,
    block TEXT NOT NULL,
    category TEXT NOT NULL,
    family TEXT NOT NULL,
    atomic_radius_pm REAL,
    first_ionization_kj_mol REAL,
    electronegativity_pauling REAL
);

CREATE TABLE isotopes (
    element_symbol TEXT NOT NULL,
    isotope TEXT PRIMARY KEY,
    atomic_number INTEGER NOT NULL,
    mass_number INTEGER NOT NULL,
    isotopic_mass_u REAL NOT NULL,
    fractional_abundance REAL NOT NULL,
    neutron_number INTEGER GENERATED ALWAYS AS (mass_number - atomic_number) VIRTUAL,
    weighted_contribution_u REAL GENERATED ALWAYS AS (isotopic_mass_u * fractional_abundance) VIRTUAL,
    FOREIGN KEY (element_symbol) REFERENCES elements(symbol)
);

CREATE TABLE classification_rules (
    rule_id INTEGER PRIMARY KEY,
    classification_layer TEXT NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO elements VALUES
('H','Hydrogen',1,1,1,'s','nonmetal','hydrogen',53,1312,2.20),
('He','Helium',2,18,1,'s','noble gas','noble gas',31,2372,NULL),
('Li','Lithium',3,1,2,'s','alkali metal','alkali metal',128,520,0.98),
('Be','Beryllium',4,2,2,'s','alkaline earth metal','alkaline earth metal',96,900,1.57),
('B','Boron',5,13,2,'p','metalloid','boron group',84,801,2.04),
('C','Carbon',6,14,2,'p','nonmetal','carbon group',76,1086,2.55),
('N','Nitrogen',7,15,2,'p','nonmetal','pnictogen',71,1402,3.04),
('O','Oxygen',8,16,2,'p','nonmetal','chalcogen',66,1314,3.44),
('F','Fluorine',9,17,2,'p','halogen','halogen',57,1681,3.98),
('Ne','Neon',10,18,2,'p','noble gas','noble gas',58,2081,NULL),
('Na','Sodium',11,1,3,'s','alkali metal','alkali metal',166,496,0.93),
('Mg','Magnesium',12,2,3,'s','alkaline earth metal','alkaline earth metal',141,738,1.31),
('Al','Aluminium',13,13,3,'p','post-transition metal','boron group',121,578,1.61),
('Si','Silicon',14,14,3,'p','metalloid','carbon group',111,787,1.90),
('P','Phosphorus',15,15,3,'p','nonmetal','pnictogen',107,1012,2.19),
('S','Sulfur',16,16,3,'p','nonmetal','chalcogen',105,1000,2.58),
('Cl','Chlorine',17,17,3,'p','halogen','halogen',102,1251,3.16),
('Ar','Argon',18,18,3,'p','noble gas','noble gas',106,1521,NULL),
('K','Potassium',19,1,4,'s','alkali metal','alkali metal',203,419,0.82),
('Ca','Calcium',20,2,4,'s','alkaline earth metal','alkaline earth metal',176,590,1.00),
('Fe','Iron',26,8,4,'d','transition metal','transition metal',156,762,1.83),
('Cu','Copper',29,11,4,'d','transition metal','transition metal',145,745,1.90),
('Zn','Zinc',30,12,4,'d','transition metal','transition metal',142,906,1.65),
('Br','Bromine',35,17,4,'p','halogen','halogen',120,1140,2.96),
('Kr','Krypton',36,18,4,'p','noble gas','noble gas',116,1351,3.00);

INSERT INTO isotopes (element_symbol,isotope,atomic_number,mass_number,isotopic_mass_u,fractional_abundance) VALUES
('C','C-12',6,12,12.00000000,0.9893),
('C','C-13',6,13,13.00335484,0.0107),
('Cl','Cl-35',17,35,34.96885268,0.7576),
('Cl','Cl-37',17,37,36.96590260,0.2424),
('Cu','Cu-63',29,63,62.92959772,0.6915),
('Cu','Cu-65',29,65,64.92778970,0.3085),
('Br','Br-79',35,79,78.9183376,0.5069),
('Br','Br-81',35,81,80.9162897,0.4931);

INSERT INTO classification_rules VALUES
(1,'identity','Atomic number defines elemental identity.'),
(2,'position','Group and period locate an element in the periodic table.'),
(3,'block','Block reflects the subshell associated with periodic placement.'),
(4,'family','Family labels summarize recurring chemical behavior.'),
(5,'property','Periodic trends support prediction but include exceptions.'),
(6,'measurement','Atomic weights depend on isotopic composition and evaluated data.'),
(7,'computation','Element descriptors can be represented as structured feature vectors.');
