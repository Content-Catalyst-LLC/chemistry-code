-- Sample queries for synthetic electroanalytical chemistry workflows.

-- 1. Calibration records ordered by concentration.
SELECT
    analyte,
    concentration_uM,
    current_uA,
    electrode_id
FROM amperometric_calibration
ORDER BY analyte, concentration_uM;

-- 2. Unknown concentration summary.
SELECT
    sample_id,
    COUNT(*) AS replicate_count,
    AVG(estimated_concentration_uM) AS mean_concentration_uM,
    AVG(current_uA) AS mean_current_uA
FROM sensor_unknown
GROUP BY sample_id
ORDER BY sample_id;

-- 3. Interference flags above a response-change threshold.
SELECT
    test_id,
    interferent,
    interferent_concentration_uM,
    response_change_percent
FROM interference_test
WHERE ABS(response_change_percent) >= 5.0
ORDER BY ABS(response_change_percent) DESC;

-- 4. Voltammetric peak current by scan rate.
SELECT
    analyte,
    scan_rate_mV_s,
    peak_potential_V,
    peak_current_uA
FROM voltammetric_peak
ORDER BY analyte, scan_rate_mV_s;
