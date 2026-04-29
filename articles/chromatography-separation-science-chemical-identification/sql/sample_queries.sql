-- Sample queries for synthetic chromatography workflows.

-- 1. Calculate retention factors for peaks.
SELECT
    p.peak_id,
    p.sample_id,
    p.retention_time_min,
    m.dead_time_min,
    (p.retention_time_min - m.dead_time_min) / m.dead_time_min AS retention_factor_k
FROM chromatographic_peak p
JOIN chromatographic_method m
    ON p.method_id = m.method_id
ORDER BY p.sample_id, p.retention_time_min;

-- 2. Review tentative identifications and caution notes.
SELECT
    ti.identification_id,
    p.peak_id,
    rc.compound_name,
    ti.retention_delta_min,
    ti.identification_status,
    ti.caution_note
FROM tentative_identification ti
JOIN chromatographic_peak p
    ON ti.peak_id = p.peak_id
JOIN reference_compound rc
    ON ti.compound_id = rc.compound_id
ORDER BY ti.retention_delta_min;

-- 3. Calibration records ordered by concentration.
SELECT
    compound_name,
    concentration_mg_l,
    peak_area,
    record_type
FROM calibration_record
ORDER BY compound_name, concentration_mg_l;

-- 4. Peak area summary by sample.
SELECT
    sample_id,
    COUNT(*) AS peak_count,
    AVG(peak_area) AS mean_peak_area,
    MAX(peak_area) AS max_peak_area
FROM chromatographic_peak
GROUP BY sample_id;
