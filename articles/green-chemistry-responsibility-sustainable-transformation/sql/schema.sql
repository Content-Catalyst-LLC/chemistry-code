-- Green Chemistry, Responsibility, and Sustainable Transformation
-- Synthetic educational schema only.
-- Not for certification, regulatory compliance, process safety, life-cycle assessment,
-- toxicity determination, product claims, or environmental marketing support.

CREATE TABLE IF NOT EXISTS green_chemistry_routes (
    route_id TEXT PRIMARY KEY,
    route_name TEXT NOT NULL,
    chemistry_class TEXT,
    product_mass_kg REAL,
    product_mw REAL,
    reactant_mw_sum REAL,
    total_input_mass_kg REAL,
    waste_mass_kg REAL,
    solvent_mass_kg REAL,
    water_mass_kg REAL,
    energy_kwh REAL,
    reaction_temperature_c REAL,
    reaction_pressure_bar REAL,
    catalyst_loading_mol_percent REAL,
    yield_fraction REAL,
    hazard_score REAL,
    solvent_hazard_score REAL,
    renewable_feedstock_fraction REAL,
    circularity_score REAL,
    degradation_score REAL,
    accident_potential_score REAL,
    realtime_monitoring_score REAL,
    qc_score REAL
);

CREATE TABLE IF NOT EXISTS green_chemistry_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id TEXT NOT NULL,
    atom_economy REAL,
    e_factor REAL,
    process_mass_intensity REAL,
    solvent_burden REAL,
    hazard_weighted_mass_intensity REAL,
    energy_intensity_kwh_per_kg_product REAL,
    catalysis_score REAL,
    process_safety_score REAL,
    green_chemistry_score REAL,
    profile_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (route_id) REFERENCES green_chemistry_routes(route_id)
);
