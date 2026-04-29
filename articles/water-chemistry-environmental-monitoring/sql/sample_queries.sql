-- Sample query 1: benchmark screening.
SELECT
    s.sample_id,
    s.sample_date,
    st.site_name,
    st.medium,
    st.water_body_type,
    a.analyte_name,
    a.analyte_group,
    m.concentration,
    m.unit,
    a.benchmark_value,
    a.benchmark_unit,
    m.concentration / a.benchmark_value AS ratio_to_benchmark,
    CASE
        WHEN m.concentration / a.benchmark_value > 1 THEN 'exceeds_benchmark'
        ELSE 'below_benchmark'
    END AS screening_flag
FROM measurements m
JOIN samples s ON m.sample_id = s.sample_id
JOIN monitoring_sites st ON s.site_id = st.site_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.benchmark_value IS NOT NULL;

-- Sample query 2: nutrient load estimates.
-- kg/day = mg/L * L/s * 0.0864
SELECT
    s.sample_id,
    s.sample_date,
    st.site_name,
    a.analyte_name,
    m.concentration,
    m.unit,
    s.flow_L_s,
    m.concentration * s.flow_L_s * 0.0864 AS load_kg_day
FROM measurements m
JOIN samples s ON m.sample_id = s.sample_id
JOIN monitoring_sites st ON s.site_id = st.site_id
JOIN analytes a ON m.analyte_id = a.analyte_id
WHERE a.analyte_name IN ('nitrate_as_N', 'phosphate_as_P', 'total_phosphorus', 'ammonia_as_N')
  AND m.unit = 'mg/L'
  AND s.flow_L_s IS NOT NULL;

-- Sample query 3: pH and conductivity field flags.
SELECT
    sample_id,
    sample_date,
    pH,
    conductivity_uS_cm,
    CASE
        WHEN pH < 6.5 OR pH > 9.0 THEN 'outside_illustrative_aquatic_range'
        ELSE 'within_illustrative_aquatic_range'
    END AS pH_flag,
    CASE
        WHEN conductivity_uS_cm > 1000 THEN 'elevated_conductivity_screen'
        ELSE 'not_elevated_screen'
    END AS conductivity_flag
FROM samples;
