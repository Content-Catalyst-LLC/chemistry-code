-- Sample queries for synthetic mass spectrometry workflows.

-- 1. Candidate matches within a specified mass-error window.
SELECT
    f.feature_id,
    f.sample_id,
    c.candidate_name,
    f.observed_mz,
    c.theoretical_mz,
    m.ppm_error,
    m.identification_status
FROM ms_candidate_match m
JOIN ms_feature f
    ON m.feature_id = f.feature_id
JOIN ms_candidate c
    ON m.candidate_id = c.candidate_id
WHERE ABS(m.ppm_error) <= 5.0
ORDER BY ABS(m.ppm_error);

-- 2. MS/MS fragment evidence by feature.
SELECT
    feature_id,
    COUNT(*) AS fragment_count,
    MAX(relative_intensity) AS max_relative_intensity
FROM msms_fragment
GROUP BY feature_id
ORDER BY feature_id;

-- 3. Feature summary by charge state.
SELECT
    charge,
    COUNT(*) AS feature_count,
    AVG(peak_area) AS mean_peak_area,
    MIN(observed_mz) AS min_mz,
    MAX(observed_mz) AS max_mz
FROM ms_feature
GROUP BY charge
ORDER BY charge;

-- 4. Calibration records ordered by concentration.
SELECT
    compound_name,
    concentration_ng_ml,
    peak_area,
    record_type
FROM ms_calibration_record
ORDER BY compound_name, concentration_ng_ml;
