-- Sample queries for synthetic materials chemistry workflows.

-- 1. Lightweight materials with moderate recyclability.
SELECT
    material_id,
    material_class,
    density_g_cm3,
    recyclability_score,
    relative_cost_score
FROM material_candidate
WHERE density_g_cm3 <= 1.5
  AND recyclability_score >= 0.60
ORDER BY recyclability_score DESC;

-- 2. High-temperature candidates.
SELECT
    material_id,
    material_class,
    thermal_stability_C,
    modulus_GPa
FROM material_candidate
WHERE thermal_stability_C >= 500
ORDER BY thermal_stability_C DESC;

-- 3. Processing conditions requiring energy review.
SELECT
    p.process_id,
    p.material_id,
    m.material_class,
    p.synthesis_route,
    p.processing_temperature_C,
    p.processing_time_h
FROM processing_condition p
JOIN material_candidate m
    ON p.material_id = m.material_id
WHERE p.processing_temperature_C >= 1000
ORDER BY p.processing_temperature_C DESC;

-- 4. Materials with lifecycle flags.
SELECT
    l.material_id,
    m.material_class,
    l.critical_element_flag,
    l.toxicity_flag,
    l.recyclability_note,
    l.processing_energy_note
FROM lifecycle_note l
JOIN material_candidate m
    ON l.material_id = m.material_id
WHERE l.critical_element_flag = 1
   OR l.toxicity_flag <> 'low'
ORDER BY l.material_id;

-- 5. Property measurements by material.
SELECT
    material_id,
    property_name,
    value,
    unit,
    method,
    temperature_C
FROM property_measurement
ORDER BY material_id, property_name;
