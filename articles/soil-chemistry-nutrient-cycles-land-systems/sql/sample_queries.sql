-- Sample query 1: soil organic carbon stock.
-- Mg C/ha = SOC_percent * bulk_density_g_cm3 * depth_cm
SELECT
    s.sample_id,
    st.site_name,
    st.land_use,
    s.depth_cm,
    s.bulk_density_g_cm3,
    m.concentration AS soc_percent,
    m.concentration * s.bulk_density_g_cm3 * s.depth_cm AS soc_stock_Mg_ha
FROM soil_measurements m
JOIN soil_samples s ON m.sample_id = s.sample_id
JOIN soil_sites st ON s.site_id = st.site_id
WHERE m.analyte = 'soil_organic_carbon_percent';

-- Sample query 2: base saturation.
SELECT
    sx.sample_id,
    sx.cec_cmolc_kg,
    sx.base_cations_cmolc_kg,
    100.0 * sx.base_cations_cmolc_kg / sx.cec_cmolc_kg AS base_saturation_percent
FROM soil_exchange_properties sx
WHERE sx.cec_cmolc_kg > 0;

-- Sample query 3: nutrient attention flags.
SELECT
    s.sample_id,
    st.site_name,
    st.land_use,
    MAX(CASE WHEN m.analyte = 'phosphorus_mg_kg' THEN m.concentration END) AS phosphorus_mg_kg,
    MAX(CASE WHEN m.analyte = 'nitrate_mg_kg' THEN m.concentration END) AS nitrate_mg_kg,
    CASE
        WHEN MAX(CASE WHEN m.analyte = 'phosphorus_mg_kg' THEN m.concentration END) > 60
        THEN 'high_phosphorus_runoff_attention'
        ELSE 'not_high_screen'
    END AS phosphorus_flag,
    CASE
        WHEN MAX(CASE WHEN m.analyte = 'nitrate_mg_kg' THEN m.concentration END) > 30
        THEN 'high_nitrate_leaching_attention'
        ELSE 'not_high_screen'
    END AS nitrate_flag
FROM soil_measurements m
JOIN soil_samples s ON m.sample_id = s.sample_id
JOIN soil_sites st ON s.site_id = st.site_id
WHERE m.analyte IN ('phosphorus_mg_kg', 'nitrate_mg_kg')
GROUP BY s.sample_id, st.site_name, st.land_use;
