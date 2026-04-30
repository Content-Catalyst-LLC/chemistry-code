-- Sample query 1: ocean carbonate screening table.
SELECT
    s.sample_id,
    s.sample_date,
    st.station_name,
    st.region,
    st.water_type,
    s.depth_m,
    c.pH_total_scale,
    c.DIC_umol_kg,
    c.total_alkalinity_umol_kg,
    c.pCO2_uatm,
    i.carbonate_umol_kg_simplified,
    i.omega_aragonite_simplified,
    i.saturation_flag
FROM ocean_samples s
JOIN ocean_stations st ON s.station_id = st.station_id
JOIN carbonate_measurements c ON s.sample_id = c.sample_id
LEFT JOIN carbonate_indicators i ON s.sample_id = i.sample_id;

-- Sample query 2: low aragonite saturation attention flags.
SELECT
    s.sample_id,
    st.station_name,
    st.water_type,
    c.pH_total_scale,
    i.omega_aragonite_simplified,
    i.carbonate_umol_kg_simplified
FROM ocean_samples s
JOIN ocean_stations st ON s.station_id = st.station_id
JOIN carbonate_measurements c ON s.sample_id = c.sample_id
JOIN carbonate_indicators i ON s.sample_id = i.sample_id
WHERE i.omega_aragonite_simplified < 2.0
ORDER BY i.omega_aragonite_simplified ASC;

-- Sample query 3: average carbonate indicators by water type.
SELECT
    st.water_type,
    COUNT(*) AS sample_count,
    AVG(c.pH_total_scale) AS mean_pH,
    AVG(c.DIC_umol_kg) AS mean_DIC_umol_kg,
    AVG(c.total_alkalinity_umol_kg) AS mean_TA_umol_kg,
    AVG(i.omega_aragonite_simplified) AS mean_omega_aragonite_simplified
FROM ocean_samples s
JOIN ocean_stations st ON s.station_id = st.station_id
JOIN carbonate_measurements c ON s.sample_id = c.sample_id
JOIN carbonate_indicators i ON s.sample_id = i.sample_id
GROUP BY st.water_type
ORDER BY mean_omega_aragonite_simplified ASC;
