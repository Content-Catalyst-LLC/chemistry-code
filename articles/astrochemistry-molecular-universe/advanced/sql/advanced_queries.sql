-- Query 1: strong molecular-line screens.
SELECT
    o.source_name,
    o.environment,
    c.species,
    c.transition_label,
    m.frequency_offset_MHz,
    m.radial_velocity_km_s,
    m.signal_to_noise,
    m.match_quality
FROM line_match_results m
JOIN observed_spectral_lines o ON m.observed_line_id = o.observed_line_id
JOIN molecular_catalog_lines c ON m.catalog_line_id = c.catalog_line_id
WHERE m.match_quality = 'strong_screen'
ORDER BY m.signal_to_noise DESC;

-- Query 2: transitions available for rotational-diagram analysis.
SELECT
    species,
    COUNT(*) AS transition_count,
    MIN(upper_energy_K) AS min_upper_energy_K,
    MAX(upper_energy_K) AS max_upper_energy_K
FROM molecular_catalog_lines
WHERE upper_energy_K IS NOT NULL
  AND g_upper IS NOT NULL
GROUP BY species
HAVING COUNT(*) >= 2;

-- Query 3: observations with velocity offsets needing review.
SELECT
    o.source_name,
    c.species,
    c.transition_label,
    m.radial_velocity_km_s,
    m.frequency_offset_MHz,
    m.match_quality
FROM line_match_results m
JOIN observed_spectral_lines o ON m.observed_line_id = o.observed_line_id
JOIN molecular_catalog_lines c ON m.catalog_line_id = c.catalog_line_id
WHERE ABS(m.radial_velocity_km_s) > 30
ORDER BY ABS(m.radial_velocity_km_s) DESC;
