-- Query 1: low aragonite saturation records.
SELECT
    s.station,
    s.region,
    s.water_type,
    m.pH_total_scale,
    m.DIC_umol_kg,
    m.total_alkalinity_umol_kg,
    i.carbonate_umol_kg,
    i.omega_aragonite_simplified,
    i.saturation_flag,
    i.acidification_pressure_index
FROM ocean_carbonate_samples s
JOIN carbonate_measurements m ON s.sample_id = m.sample_id
JOIN carbonate_indicators i ON s.sample_id = i.sample_id
WHERE i.omega_aragonite_simplified < 2.0
ORDER BY i.omega_aragonite_simplified ASC;

-- Query 2: water-type summary.
SELECT
    s.water_type,
    COUNT(*) AS n,
    AVG(m.pH_total_scale) AS mean_pH,
    AVG(m.DIC_umol_kg) AS mean_DIC,
    AVG(m.total_alkalinity_umol_kg) AS mean_TA,
    AVG(i.omega_aragonite_simplified) AS mean_omega_aragonite,
    AVG(i.acidification_pressure_index) AS mean_pressure_index
FROM ocean_carbonate_samples s
JOIN carbonate_measurements m ON s.sample_id = m.sample_id
JOIN carbonate_indicators i ON s.sample_id = i.sample_id
GROUP BY s.water_type
ORDER BY mean_pressure_index DESC;

-- Query 3: DIC sensitivity where modeled aragonite saturation drops below 2.
SELECT
    s.station,
    r.added_DIC_umol_kg,
    r.modeled_pH_total_scale,
    r.modeled_carbonate_umol_kg,
    r.modeled_omega_aragonite
FROM carbonate_sensitivity_runs r
JOIN ocean_carbonate_samples s ON r.sample_id = s.sample_id
WHERE r.modeled_omega_aragonite < 2.0
ORDER BY r.added_DIC_umol_kg ASC;
