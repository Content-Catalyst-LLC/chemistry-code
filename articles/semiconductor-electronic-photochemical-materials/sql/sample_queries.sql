-- Sample queries for synthetic semiconductor, electronic, and photochemical materials workflows.

-- 1. Candidate materials with visible-to-near-infrared band gaps.
SELECT
    material_id,
    material_class,
    band_gap_eV,
    absorption_edge_nm,
    photostability_score,
    critical_material_flag
FROM material_candidate
WHERE band_gap_eV BETWEEN 1.2 AND 2.3
ORDER BY photostability_score DESC;

-- 2. Device-like replicate summary.
SELECT
    material_id,
    COUNT(*) AS replicate_count,
    AVG(photocurrent_mA_cm2) AS mean_photocurrent_mA_cm2,
    AVG(open_circuit_voltage_V) AS mean_open_circuit_voltage_V,
    AVG(fill_factor) AS mean_fill_factor,
    AVG(photostability_score) AS mean_photostability_score
FROM device_run
GROUP BY material_id
ORDER BY mean_photostability_score DESC;

-- 3. Materials requiring interface review.
SELECT
    m.material_id,
    m.material_class,
    i.interface_type,
    i.dominant_issue,
    i.mitigation_strategy
FROM interface_record i
JOIN material_candidate m
    ON i.material_id = m.material_id
WHERE i.review_required = 1
ORDER BY m.material_id;

-- 4. Photostability records with significant loss.
SELECT
    material_id,
    illumination_hours,
    normalized_performance,
    stress_condition
FROM photostability_time_series
WHERE normalized_performance < 0.70
ORDER BY material_id, illumination_hours;

-- 5. Responsible design and lifecycle review.
SELECT
    m.material_id,
    m.material_class,
    l.critical_material_flag,
    l.toxicity_or_exposure_concern,
    l.processing_energy_review,
    l.end_of_life_note
FROM lifecycle_note l
JOIN material_candidate m
    ON l.material_id = m.material_id
WHERE l.responsible_design_review = 1
ORDER BY m.material_id;
