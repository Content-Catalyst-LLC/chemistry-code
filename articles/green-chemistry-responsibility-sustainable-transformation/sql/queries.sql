-- Highest-scoring synthetic green chemistry routes.
SELECT
    r.route_name,
    r.chemistry_class,
    i.atom_economy,
    i.e_factor,
    i.process_mass_intensity,
    i.hazard_weighted_mass_intensity,
    i.green_chemistry_score,
    i.profile_flag
FROM green_chemistry_indicators i
JOIN green_chemistry_routes r ON i.route_id = r.route_id
ORDER BY i.green_chemistry_score DESC;

-- Route-class summary.
SELECT
    r.chemistry_class,
    COUNT(*) AS n,
    AVG(i.atom_economy) AS mean_atom_economy,
    AVG(i.e_factor) AS mean_e_factor,
    AVG(i.process_mass_intensity) AS mean_pmi,
    AVG(i.green_chemistry_score) AS mean_green_score
FROM green_chemistry_indicators i
JOIN green_chemistry_routes r ON i.route_id = r.route_id
GROUP BY r.chemistry_class
ORDER BY mean_green_score DESC;
