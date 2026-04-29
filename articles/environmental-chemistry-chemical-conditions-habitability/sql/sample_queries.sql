-- Sample query 1: benchmark screening.
SELECT
    s.sample_id,
    s.sample_date,
    st.site_name,
    s.medium,
    a.analyte_name,
    m.concentration,
    m.unit,
    a.benchmark_value,
    a.benchmark_unit,
    m.concentration / a.benchmark_value AS hazard_quotient,
    CASE
        WHEN m.concentration / a.benchmark_value > 1 THEN 'exceeds_benchmark'
        ELSE 'below_benchmark'
    END AS screening_flag
FROM measurements m
JOIN samples s ON m.sample_id = s.sample_id
JOIN monitoring_sites st ON s.site_id = st.site_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.benchmark_value IS NOT NULL;

-- Sample query 2: exceedance counts by medium.
SELECT
    s.medium,
    COUNT(*) AS measurement_count,
    SUM(CASE WHEN m.concentration > a.benchmark_value THEN 1 ELSE 0 END) AS exceedance_count
FROM measurements m
JOIN samples s ON m.sample_id = s.sample_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.benchmark_value IS NOT NULL
GROUP BY s.medium
ORDER BY exceedance_count DESC;

-- Sample query 3: quality-control flags.
SELECT
    s.sample_id,
    st.site_name,
    s.medium,
    a.analyte_name,
    m.concentration,
    m.unit,
    m.detection_limit,
    m.qc_flag
FROM measurements m
JOIN samples s ON m.sample_id = s.sample_id
JOIN monitoring_sites st ON s.site_id = st.site_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE m.qc_flag IS NOT NULL;
