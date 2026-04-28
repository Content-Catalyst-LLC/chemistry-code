DROP TABLE IF EXISTS pair_potential_parameters;
DROP TABLE IF EXISTS vapor_pressure_measurements;
DROP TABLE IF EXISTS surface_tension_measurements;
DROP TABLE IF EXISTS phase_properties;
DROP TABLE IF EXISTS particle_coordinates;
DROP TABLE IF EXISTS workflow_steps;

CREATE TABLE pair_potential_parameters (
    pair TEXT PRIMARY KEY,
    epsilon_kj_mol REAL NOT NULL,
    sigma_angstrom REAL NOT NULL,
    interaction_note TEXT NOT NULL
);

CREATE TABLE vapor_pressure_measurements (
    substance TEXT NOT NULL,
    temperature_K REAL NOT NULL,
    pressure_kPa REAL NOT NULL,
    inverse_temperature_K_inv REAL GENERATED ALWAYS AS (1.0 / temperature_K) VIRTUAL
);

CREATE TABLE surface_tension_measurements (
    liquid TEXT PRIMARY KEY,
    surface_tension_mN_m REAL NOT NULL,
    dominant_interaction TEXT NOT NULL
);

CREATE TABLE phase_properties (
    substance TEXT PRIMARY KEY,
    molecular_mass_g_mol REAL NOT NULL,
    dominant_interaction TEXT NOT NULL,
    phase_at_room_conditions TEXT NOT NULL,
    boiling_point_C REAL,
    melting_point_C REAL
);

CREATE TABLE particle_coordinates (
    particle INTEGER PRIMARY KEY,
    x_nm REAL NOT NULL,
    y_nm REAL NOT NULL,
    z_nm REAL NOT NULL
);

CREATE TABLE workflow_steps (
    step_id INTEGER PRIMARY KEY,
    operation TEXT NOT NULL,
    input_artifact TEXT NOT NULL,
    script TEXT NOT NULL,
    output_artifact TEXT NOT NULL,
    notes TEXT NOT NULL
);

INSERT INTO pair_potential_parameters VALUES
('argon_argon',0.997,3.40,'simplified noble gas Lennard-Jones pair'),
('methane_methane',1.230,3.73,'simplified nonpolar molecular pair'),
('carbon_dioxide_carbon_dioxide',1.650,3.90,'simplified quadrupolar molecule represented with LJ scaffold'),
('water_oxygen_water_oxygen',0.650,3.15,'simplified water oxygen site scaffold');

INSERT INTO vapor_pressure_measurements (substance, temperature_K, pressure_kPa) VALUES
('synthetic_liquid',290,1.9),
('synthetic_liquid',300,3.0),
('synthetic_liquid',310,4.6),
('synthetic_liquid',320,6.9),
('synthetic_liquid',330,10.1),
('synthetic_liquid',340,14.5);

INSERT INTO surface_tension_measurements VALUES
('water',72.0,'hydrogen bonding network'),
('ethanol',22.0,'hydrogen bonding and dispersion'),
('hexane',18.4,'dispersion'),
('glycerol',63.0,'extensive hydrogen bonding');

INSERT INTO phase_properties VALUES
('water',18.015,'hydrogen bonding','liquid',100.0,0.0),
('methane',16.043,'dispersion','gas',-161.5,-182.5),
('carbon_dioxide',44.010,'dispersion and quadrupolar','gas',-78.5,-56.6),
('ethanol',46.069,'hydrogen bonding and dispersion','liquid',78.4,-114.1),
('iodine',253.808,'dispersion','solid',184.3,113.7);

INSERT INTO particle_coordinates VALUES
(1,0.0,0.0,0.0),
(2,1.0,0.2,0.1),
(3,0.9,1.1,-0.2),
(4,-1.1,0.1,1.0),
(5,-0.8,-1.0,-0.3),
(6,2.0,0.4,0.5),
(7,-2.1,-0.2,0.6),
(8,0.1,2.2,-0.7),
(9,1.8,1.8,0.2),
(10,-1.9,-1.7,-0.4);

INSERT INTO workflow_steps VALUES
(1,'lennard_jones_potential','pair_potential_parameters.csv','python/01_lennard_jones_potential.py','outputs/tables/lennard_jones_potentials.csv','Calculate LJ potential curves and minima'),
(2,'vapor_pressure_fit','vapor_pressure_sample.csv','python/02_vapor_pressure_fit.py','outputs/tables/vapor_pressure_fit.csv','Fit Clausius-Clapeyron-style relation'),
(3,'radial_distribution_scaffold','particle_coordinates.csv','python/03_radial_distribution_scaffold.py','outputs/tables/radial_distribution_scaffold.csv','Create pair-distance histogram scaffold'),
(4,'phase_property_summary','phase_properties_sample.csv;surface_tension_sample.csv','python/04_phase_property_summary.py','outputs/tables/phase_property_summary.csv','Summarize condensed-matter property tables'),
(5,'provenance','workflow_manifest.csv','python/05_provenance_manifest.py','outputs/manifests/provenance_manifest.csv','Record workflow checksums'),
(6,'report','multiple outputs','python/06_generate_condensed_matter_report.py','outputs/reports/intermolecular_forces_report.md','Generate report');
