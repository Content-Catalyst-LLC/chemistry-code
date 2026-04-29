-- Sample queries for synthetic surface chemistry and catalysis workflows.

-- 1. High-selectivity catalyst candidates.
SELECT
    catalyst_id,
    catalyst_class,
    surface_area_m2_g,
    site_density_umol_g,
    selectivity_target,
    critical_metal_flag
FROM catalyst_candidate
WHERE selectivity_target >= 0.85
ORDER BY selectivity_target DESC;

-- 2. Adsorption coverage by pressure.
SELECT
    catalyst_id,
    adsorbate,
    pressure_bar,
    coverage_fraction,
    temperature_K
FROM adsorption_isotherm
ORDER BY catalyst_id, pressure_bar;

-- 3. Catalyst performance replicate summary.
SELECT
    catalyst_id,
    COUNT(*) AS replicate_count,
    AVG(conversion_percent) AS mean_conversion_percent,
    AVG(selectivity_percent) AS mean_selectivity_percent
FROM catalyst_performance
GROUP BY catalyst_id
ORDER BY mean_selectivity_percent DESC;

-- 4. Sustainability review flags.
SELECT
    l.catalyst_id,
    c.catalyst_class,
    l.critical_material_flag,
    l.toxicity_flag,
    l.regeneration_note,
    l.end_of_life_note
FROM lifecycle_note l
JOIN catalyst_candidate c
    ON l.catalyst_id = c.catalyst_id
WHERE l.sustainability_review_required = 1
ORDER BY l.catalyst_id;

-- 5. Surface characterization by catalyst.
SELECT
    catalyst_id,
    method,
    measurement_target,
    value,
    unit,
    condition
FROM surface_characterization
ORDER BY catalyst_id, method;
