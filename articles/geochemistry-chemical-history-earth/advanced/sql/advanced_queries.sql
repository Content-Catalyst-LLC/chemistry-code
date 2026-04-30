-- Query 1: strongest geochemical archive signals.
SELECT
    s.sample_id,
    s.location,
    s.rock_type,
    s.geologic_context,
    i.CIA_molar_CaO_star,
    i.Rb_Sr_ratio,
    i.LaN_YbN_ratio,
    i.redox_archive_index,
    i.geochemical_archive_index,
    i.attention_flag
FROM geochemical_samples s
JOIN geochemical_indicators i ON s.sample_id = i.sample_id
ORDER BY i.geochemical_archive_index DESC;

-- Query 2: high weathering screens.
SELECT
    s.sample_id,
    s.location,
    s.material,
    s.rock_type,
    i.CIA_molar_CaO_star,
    i.Rb_Sr_ratio,
    i.attention_flag
FROM geochemical_samples s
JOIN geochemical_indicators i ON s.sample_id = i.sample_id
WHERE i.CIA_molar_CaO_star >= 80
ORDER BY i.CIA_molar_CaO_star DESC;

-- Query 3: rock-type indicator summaries.
SELECT
    s.rock_type,
    COUNT(*) AS n,
    AVG(i.CIA_molar_CaO_star) AS mean_CIA,
    AVG(i.Rb_Sr_ratio) AS mean_Rb_Sr,
    AVG(i.redox_archive_index) AS mean_redox_index,
    AVG(i.geochemical_archive_index) AS mean_archive_index
FROM geochemical_samples s
JOIN geochemical_indicators i ON s.sample_id = i.sample_id
GROUP BY s.rock_type
ORDER BY mean_archive_index DESC;

-- Query 4: simplified radiometric model outputs.
SELECT
    s.sample_id,
    s.rock_type,
    r.parent_isotope_units,
    r.radiogenic_daughter_units,
    r.decay_constant_per_year,
    r.age_Ma_simplified,
    r.assumption_note
FROM radiometric_model_outputs r
LEFT JOIN geochemical_samples s ON r.sample_id = s.sample_id
ORDER BY r.age_Ma_simplified DESC;
