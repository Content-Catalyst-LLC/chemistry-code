-- Circular Chemistry, Waste, and Material Futures
-- Synthetic educational schema only.
-- Not for recycling certification, waste-management approval, regulatory compliance,
-- LCA, toxicology, food-contact suitability, or product-claim support.

CREATE TABLE IF NOT EXISTS circular_material_streams (
    stream_id TEXT PRIMARY KEY,
    material_stream TEXT NOT NULL,
    material_class TEXT,
    recovery_pathway TEXT,
    input_waste_kg REAL,
    recovered_useful_kg REAL,
    recovered_quality_factor REAL,
    substitution_factor REAL,
    energy_kwh REAL,
    solvent_or_reagent_kg REAL,
    process_water_kg REAL,
    hazard_score REAL,
    exposure_relevance REAL,
    contamination_score REAL,
    traceability_score REAL,
    collection_rate REAL,
    sorting_efficiency REAL,
    reuse_cycles REAL,
    loss_fraction_per_cycle REAL,
    critical_material_fraction REAL,
    worker_exposure_score REAL,
    qc_score REAL
);

CREATE TABLE IF NOT EXISTS circular_chemistry_indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stream_id TEXT NOT NULL,
    recovery_yield REAL,
    circular_retention REAL,
    material_remaining_after_cycles_kg REAL,
    hazard_weighted_recovered_flow REAL,
    energy_intensity_kwh_per_kg_recovered REAL,
    reagent_intensity_kg_per_kg_recovered REAL,
    water_intensity_kg_per_kg_recovered REAL,
    infrastructure_score REAL,
    safe_circularity_score REAL,
    circular_chemistry_score REAL,
    profile_flag TEXT,
    model_version TEXT,
    FOREIGN KEY (stream_id) REFERENCES circular_material_streams(stream_id)
);
