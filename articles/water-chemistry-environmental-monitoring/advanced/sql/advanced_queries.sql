-- Query 1: highest water-quality pressure records.
SELECT
    s.sample_id,
    st.site_name,
    st.water_body_type,
    m.analyte,
    m.concentration,
    m.benchmark,
    m.unit,
    i.benchmark_ratio,
    i.load_kg_day,
    i.oxygen_stress_index,
    i.nutrient_enrichment_index,
    i.metal_pressure_index,
    i.water_quality_pressure_index,
    i.attention_flag
FROM water_advanced_indicators i
JOIN water_samples s ON i.sample_id = s.sample_id
JOIN water_sites st ON s.site_id = st.site_id
JOIN water_measurements m ON s.sample_id = m.sample_id
ORDER BY i.water_quality_pressure_index DESC;

-- Query 2: benchmark exceedances.
SELECT
    s.sample_id,
    st.site_name,
    st.water_body_type,
    m.analyte,
    m.concentration,
    m.benchmark,
    m.unit,
    i.benchmark_ratio,
    i.attention_flag
FROM water_advanced_indicators i
JOIN water_samples s ON i.sample_id = s.sample_id
JOIN water_sites st ON s.site_id = st.site_id
JOIN water_measurements m ON s.sample_id = m.sample_id
WHERE i.benchmark_ratio > 1.0
ORDER BY i.benchmark_ratio DESC;

-- Query 3: water-body summary.
SELECT
    st.water_body_type,
    COUNT(*) AS n,
    AVG(i.oxygen_stress_index) AS mean_oxygen_stress,
    AVG(i.nutrient_enrichment_index) AS mean_nutrient_enrichment,
    AVG(i.metal_pressure_index) AS mean_metal_pressure,
    AVG(i.water_quality_pressure_index) AS mean_pressure_index,
    SUM(i.load_kg_day) AS total_load_kg_day
FROM water_advanced_indicators i
JOIN water_samples s ON i.sample_id = s.sample_id
JOIN water_sites st ON s.site_id = st.site_id
GROUP BY st.water_body_type
ORDER BY mean_pressure_index DESC;

-- Query 4: scenario outputs.
SELECT
    scenario_type,
    scenario_name,
    time_step,
    variable_name,
    variable_value,
    variable_unit
FROM water_scenario_outputs
ORDER BY scenario_type, scenario_name, time_step;
