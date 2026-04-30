-- Advanced food chemistry and nutrition provenance schema.
-- Educational only. Not a dietary advice system, clinical nutrition system,
-- food-safety certification database, allergen clearance database,
-- regulatory compliance system, or product health-claim support system.

CREATE TABLE IF NOT EXISTS foods (
    food_id TEXT PRIMARY KEY,
    food_name TEXT NOT NULL,
    food_group TEXT,
    processing_level TEXT,
    food_matrix TEXT,
    data_quality_score REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS nutrient_composition (
    composition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id TEXT NOT NULL,
    nutrient_name TEXT NOT NULL,
    nutrient_value REAL,
    nutrient_unit TEXT,
    method_note TEXT,
    FOREIGN KEY (food_id) REFERENCES foods(food_id)
);

CREATE TABLE IF NOT EXISTS food_matrix_properties (
    food_id TEXT PRIMARY KEY,
    water_activity REAL,
    pH REAL,
    particle_accessibility REAL,
    processing_intensity REAL,
    fermentation_factor REAL,
    retention_factor REAL,
    protein_digestibility_factor REAL,
    iron_bioavailability_factor REAL,
    lipid_unsaturation_index REAL,
    oxidation_protection_factor REAL,
    FOREIGN KEY (food_id) REFERENCES foods(food_id)
);

CREATE TABLE IF NOT EXISTS food_chemistry_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id TEXT NOT NULL,
    energy_density_kcal_per_g REAL,
    nutrient_density_score REAL,
    bioavailable_iron_mg REAL,
    retained_vitamin_c_mg REAL,
    digestible_protein_g REAL,
    protein_quality_proxy REAL,
    food_matrix_protection_index REAL,
    glycemic_accessibility_proxy REAL,
    lipid_oxidation_vulnerability REAL,
    chemical_safety_attention_index REAL,
    nutrition_chemistry_quality_index REAL,
    profile_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (food_id) REFERENCES foods(food_id)
);

CREATE TABLE IF NOT EXISTS food_chemistry_scenario_outputs (
    scenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id TEXT,
    scenario_type TEXT NOT NULL,
    scenario_name TEXT,
    variable_name TEXT,
    variable_value REAL,
    variable_unit TEXT,
    assumption_note TEXT,
    FOREIGN KEY (food_id) REFERENCES foods(food_id)
);
