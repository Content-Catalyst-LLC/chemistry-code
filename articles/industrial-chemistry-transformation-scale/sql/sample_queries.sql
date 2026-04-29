-- Sample queries for synthetic industrial chemistry and scale-up workflows.

-- 1. Process route metrics.
SELECT
    route_id,
    process_type,
    actual_product_kg / theoretical_product_kg AS yield_fraction,
    waste_kg / actual_product_kg AS e_factor,
    solvent_kg / actual_product_kg AS solvent_intensity,
    energy_kWh / actual_product_kg AS energy_intensity_kWh_kg,
    actual_product_kg / (reactor_volume_m3 * batch_or_residence_time_h) AS space_time_yield_kg_m3_h
FROM process_route
ORDER BY e_factor ASC;

-- 2. Routes requiring scale-up review.
SELECT
    route_id,
    process_type,
    hazard_score,
    separation_difficulty_score,
    waste_kg / actual_product_kg AS e_factor,
    solvent_kg / actual_product_kg AS solvent_intensity
FROM process_route
WHERE hazard_score > 0.60
   OR separation_difficulty_score > 0.70
   OR waste_kg / actual_product_kg > 1.0
   OR solvent_kg / actual_product_kg > 2.0
ORDER BY hazard_score DESC, separation_difficulty_score DESC;

-- 3. Batch quality summary.
SELECT
    route_id,
    COUNT(*) AS batch_count,
    AVG(yield_fraction) AS mean_yield_fraction,
    MIN(yield_fraction) AS min_yield_fraction,
    AVG(impurity_percent) AS mean_impurity_percent,
    MAX(impurity_percent) AS max_impurity_percent
FROM batch_data
GROUP BY route_id
ORDER BY mean_yield_fraction DESC;

-- 4. Unit operations with high energy or quality-critical flags.
SELECT
    route_id,
    operation_type,
    energy_kWh,
    water_m3,
    solvent_loss_kg,
    quality_critical_flag
FROM unit_operation
WHERE energy_kWh > 300
   OR quality_critical_flag = 1
ORDER BY route_id, energy_kWh DESC;

-- 5. Decarbonization pathway priority proxy.
SELECT
    route_id,
    pathway,
    energy_reduction_percent,
    emissions_reduction_percent,
    implementation_difficulty_score,
    capital_intensity_score,
    (0.45 * energy_reduction_percent + 0.55 * emissions_reduction_percent - 10 * implementation_difficulty_score - 6 * capital_intensity_score) AS priority_score
FROM decarbonization_pathway
ORDER BY priority_score DESC;
