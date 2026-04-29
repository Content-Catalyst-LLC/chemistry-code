-- SQL schema for synthetic industrial chemistry and scale-up records.
-- Educational only; adapt and validate before real process development or plant operation.

CREATE TABLE IF NOT EXISTS process_route (
    route_id TEXT PRIMARY KEY,
    process_type TEXT NOT NULL,
    theoretical_product_kg REAL,
    actual_product_kg REAL,
    waste_kg REAL,
    solvent_kg REAL,
    energy_kWh REAL,
    reactor_volume_m3 REAL,
    batch_or_residence_time_h REAL,
    hazard_score REAL,
    separation_difficulty_score REAL,
    feedstock_risk_score REAL
);

CREATE TABLE IF NOT EXISTS batch_data (
    batch_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    yield_fraction REAL,
    impurity_percent REAL,
    energy_kWh_kg REAL,
    solvent_intensity REAL,
    temperature_deviation_C REAL,
    FOREIGN KEY (route_id) REFERENCES process_route(route_id)
);

CREATE TABLE IF NOT EXISTS unit_operation (
    operation_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    operation_type TEXT,
    energy_kWh REAL,
    water_m3 REAL,
    solvent_loss_kg REAL,
    quality_critical_flag INTEGER,
    FOREIGN KEY (route_id) REFERENCES process_route(route_id)
);

CREATE TABLE IF NOT EXISTS hazard_register (
    hazard_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    hazard_type TEXT,
    severity_score REAL,
    likelihood_score REAL,
    safeguard_score REAL,
    review_required INTEGER,
    FOREIGN KEY (route_id) REFERENCES process_route(route_id)
);

CREATE TABLE IF NOT EXISTS decarbonization_pathway (
    pathway_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    pathway TEXT,
    energy_reduction_percent REAL,
    emissions_reduction_percent REAL,
    implementation_difficulty_score REAL,
    capital_intensity_score REAL,
    FOREIGN KEY (route_id) REFERENCES process_route(route_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_note (
    note_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    feedstock_type TEXT,
    waste_management_note TEXT,
    process_safety_note TEXT,
    responsible_scale_review INTEGER,
    FOREIGN KEY (route_id) REFERENCES process_route(route_id)
);
