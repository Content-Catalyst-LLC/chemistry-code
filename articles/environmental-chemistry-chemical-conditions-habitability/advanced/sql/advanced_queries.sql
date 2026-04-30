-- Query 1: highest chemical habitability pressure records.
SELECT
    s.sample_id,
    site.site_name,
    site.compartment,
    m.analyte,
    m.analyte_class,
    m.concentration,
    m.benchmark,
    m.unit,
    i.benchmark_ratio,
    f.Kd_L_kg,
    f.retardation_factor_proxy,
    f.persistence_factor,
    i.monte_carlo_exceedance_probability,
    i.chemical_habitability_pressure_index,
    i.attention_flag
FROM environmental_advanced_indicators i
JOIN environmental_samples s ON i.sample_id = s.sample_id
JOIN environmental_sites site ON s.site_id = site.site_id
JOIN chemical_measurements m ON s.sample_id = m.sample_id
LEFT JOIN fate_transport_properties f ON s.sample_id = f.sample_id
ORDER BY i.chemical_habitability_pressure_index DESC;

-- Query 2: benchmark exceedances with high exceedance probability.
SELECT
    site.site_name,
    site.compartment,
    m.analyte,
    m.concentration,
    m.benchmark,
    m.unit,
    i.benchmark_ratio,
    i.monte_carlo_exceedance_probability,
    i.attention_flag
FROM environmental_advanced_indicators i
JOIN environmental_samples s ON i.sample_id = s.sample_id
JOIN environmental_sites site ON s.site_id = site.site_id
JOIN chemical_measurements m ON s.sample_id = m.sample_id
WHERE i.benchmark_ratio > 1.0
  AND i.monte_carlo_exceedance_probability >= 0.80
ORDER BY i.monte_carlo_exceedance_probability DESC;

-- Query 3: compartment summary.
SELECT
    site.compartment,
    COUNT(*) AS n,
    AVG(i.benchmark_ratio) AS mean_benchmark_ratio,
    AVG(f.Kd_L_kg) AS mean_Kd_L_kg,
    AVG(f.retardation_factor_proxy) AS mean_retardation_factor,
    AVG(f.persistence_factor) AS mean_persistence_factor,
    AVG(i.contaminant_pressure_index) AS mean_contaminant_pressure,
    AVG(i.chemical_habitability_pressure_index) AS mean_habitability_pressure
FROM environmental_advanced_indicators i
JOIN environmental_samples s ON i.sample_id = s.sample_id
JOIN environmental_sites site ON s.site_id = site.site_id
LEFT JOIN fate_transport_properties f ON s.sample_id = f.sample_id
GROUP BY site.compartment
ORDER BY mean_habitability_pressure DESC;

-- Query 4: scenario outputs.
SELECT
    scenario_type,
    scenario_name,
    time_step,
    variable_name,
    variable_value,
    variable_unit
FROM environmental_scenario_outputs
ORDER BY scenario_type, scenario_name, time_step;
