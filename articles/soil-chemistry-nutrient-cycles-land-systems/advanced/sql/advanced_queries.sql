-- Query 1: highest soil land-system pressure records.
SELECT
    s.sample_id,
    st.site_name,
    st.land_use,
    i.soc_stock_Mg_ha,
    i.nitrate_leaching_vulnerability,
    i.phosphorus_export_kg_ha_proxy,
    i.contaminant_pressure,
    i.soil_land_system_pressure_index,
    i.attention_flag
FROM soil_advanced_indicators i
JOIN soil_samples s ON i.sample_id = s.sample_id
JOIN soil_sites st ON s.site_id = st.site_id
ORDER BY i.soil_land_system_pressure_index DESC;

-- Query 2: land-use summaries.
SELECT
    st.land_use,
    COUNT(*) AS n,
    AVG(i.soc_stock_Mg_ha) AS mean_soc_stock_Mg_ha,
    AVG(e.base_saturation_percent) AS mean_base_saturation_percent,
    AVG(i.nitrate_leaching_vulnerability) AS mean_nitrate_leaching_vulnerability,
    AVG(i.phosphorus_export_kg_ha_proxy) AS mean_phosphorus_export_kg_ha,
    AVG(i.soil_land_system_pressure_index) AS mean_pressure_index
FROM soil_advanced_indicators i
JOIN soil_samples s ON i.sample_id = s.sample_id
JOIN soil_sites st ON s.site_id = st.site_id
LEFT JOIN soil_exchange_properties e ON s.sample_id = e.sample_id
GROUP BY st.land_use
ORDER BY mean_pressure_index DESC;

-- Query 3: high phosphorus export proxy records.
SELECT
    s.sample_id,
    st.site_name,
    st.land_use,
    i.phosphorus_export_kg_ha_proxy,
    i.annual_P_balance_kg_ha,
    i.attention_flag
FROM soil_advanced_indicators i
JOIN soil_samples s ON i.sample_id = s.sample_id
JOIN soil_sites st ON s.site_id = st.site_id
WHERE i.phosphorus_export_kg_ha_proxy >= 4.0
ORDER BY i.phosphorus_export_kg_ha_proxy DESC;

-- Query 4: scenario outputs by type.
SELECT
    scenario_type,
    scenario_name,
    scenario_year,
    variable_name,
    variable_value,
    variable_unit
FROM soil_scenario_outputs
ORDER BY scenario_type, scenario_name, scenario_year;
