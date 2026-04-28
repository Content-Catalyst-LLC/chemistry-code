DROP TABLE IF EXISTS elements;
DROP TABLE IF EXISTS isotopes;
DROP TABLE IF EXISTS compounds;
DROP TABLE IF EXISTS mole_examples;

CREATE TABLE elements (
    symbol TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    atomic_number INTEGER NOT NULL,
    period INTEGER NOT NULL,
    "group" INTEGER,
    block TEXT NOT NULL,
    category TEXT NOT NULL,
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
    FOREIGN KEY (element_symbol) REFERENCES elements(symbol)
);

CREATE TABLE compounds (
    compound TEXT NOT NULL,
    formula TEXT NOT NULL,
    element_symbol TEXT NOT NULL,
    atom_count INTEGER NOT NULL,
    atomic_mass_u REAL NOT NULL,
    element_mass_contribution REAL GENERATED ALWAYS AS (atom_count * atomic_mass_u) VIRTUAL
);

CREATE TABLE mole_examples (
    sample TEXT PRIMARY KEY,
    entity TEXT NOT NULL,
    mass_g REAL NOT NULL,
    molar_mass_g_mol REAL NOT NULL,
    amount_mol REAL GENERATED ALWAYS AS (mass_g / molar_mass_g_mol) VIRTUAL
);

INSERT INTO elements VALUES
('H','Hydrogen',1,1,1,'s','nonmetal',53,1312,2.20),
('Li','Lithium',3,2,1,'s','alkali metal',128,520,0.98),
('Be','Beryllium',4,2,2,'s','alkaline earth metal',96,900,1.57),
('B','Boron',5,2,13,'p','metalloid',84,801,2.04),
('C','Carbon',6,2,14,'p','nonmetal',76,1086,2.55),
('N','Nitrogen',7,2,15,'p','nonmetal',71,1402,3.04),
('O','Oxygen',8,2,16,'p','nonmetal',66,1314,3.44),
('F','Fluorine',9,2,17,'p','halogen',57,1681,3.98),
('Ne','Neon',10,2,18,'p','noble gas',58,2081,NULL),
('Na','Sodium',11,3,1,'s','alkali metal',166,496,0.93),
('Mg','Magnesium',12,3,2,'s','alkaline earth metal',141,738,1.31),
('Al','Aluminium',13,3,13,'p','post-transition metal',121,578,1.61),
('Si','Silicon',14,3,14,'p','metalloid',111,787,1.90),
('P','Phosphorus',15,3,15,'p','nonmetal',107,1012,2.19),
('S','Sulfur',16,3,16,'p','nonmetal',105,1000,2.58),
('Cl','Chlorine',17,3,17,'p','halogen',102,1251,3.16),
('Ar','Argon',18,3,18,'p','noble gas',106,1521,NULL),
('Fe','Iron',26,4,8,'d','transition metal',156,762,1.83),
('Cu','Copper',29,4,11,'d','transition metal',145,745,1.90),
('Zn','Zinc',30,4,12,'d','transition metal',142,906,1.65);

INSERT INTO isotopes (element_symbol,isotope,atomic_number,mass_number,isotopic_mass_u,fractional_abundance) VALUES
('C','C-12',6,12,12.00000000,0.9893),
('C','C-13',6,13,13.00335484,0.0107),
('Cl','Cl-35',17,35,34.96885268,0.7576),
('Cl','Cl-37',17,37,36.96590260,0.2424),
('Cu','Cu-63',29,63,62.92959772,0.6915),
('Cu','Cu-65',29,65,64.92778970,0.3085);

INSERT INTO compounds (compound,formula,element_symbol,atom_count,atomic_mass_u) VALUES
('water','H2O','H',2,1.008),
('water','H2O','O',1,15.999),
('carbon_dioxide','CO2','C',1,12.011),
('carbon_dioxide','CO2','O',2,15.999),
('sodium_chloride','NaCl','Na',1,22.990),
('sodium_chloride','NaCl','Cl',1,35.45),
('glucose','C6H12O6','C',6,12.011),
('glucose','C6H12O6','H',12,1.008),
('glucose','C6H12O6','O',6,15.999);

INSERT INTO mole_examples VALUES
('water_sample','H2O',18.015,18.015),
('carbon_dioxide_sample','CO2',44.010,44.010),
('sodium_chloride_sample','NaCl',58.440,58.440),
('glucose_sample','C6H12O6',180.156,180.156);
