-- Sample query 1: concentration/reference screening.
SELECT
    s.sample_id,
    s.sample_date,
    st.site_name,
    st.site_type,
    a.analyte_name,
    a.chemical_class,
    m.concentration,
    m.unit,
    a.reference_value,
    a.reference_unit,
    m.concentration / a.reference_value AS ratio_to_reference,
    CASE
        WHEN m.concentration / a.reference_value > 1 THEN 'above_reference'
        ELSE 'at_or_below_reference'
    END AS screening_flag
FROM atmospheric_measurements m
JOIN atmospheric_samples s ON m.sample_id = s.sample_id
JOIN monitoring_sites st ON s.site_id = st.site_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.reference_value IS NOT NULL;

-- Sample query 2: above-reference counts by chemical class.
SELECT
    a.chemical_class,
    COUNT(*) AS measurement_count,
    SUM(CASE WHEN m.concentration > a.reference_value THEN 1 ELSE 0 END) AS above_reference_count
FROM atmospheric_measurements m
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.reference_value IS NOT NULL
GROUP BY a.chemical_class
ORDER BY above_reference_count DESC;

-- Sample query 3: site-level ozone and PM screening context.
SELECT
    st.site_name,
    s.sample_date,
    a.analyte_name,
    m.concentration,
    m.unit,
    s.averaging_period,
    s.temperature_c,
    s.relative_humidity_percent,
    s.wind_speed_m_s
FROM atmospheric_measurements m
JOIN atmospheric_samples s ON m.sample_id = s.sample_id
JOIN monitoring_sites st ON s.site_id = st.site_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.analyte_name IN ('O3', 'PM2.5')
ORDER BY s.sample_date, st.site_name;
