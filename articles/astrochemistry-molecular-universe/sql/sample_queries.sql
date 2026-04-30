-- Sample query 1: molecular abundance and velocity screening.
SELECT
    o.observation_id,
    s.source_name,
    s.environment,
    m.species_name,
    o.rest_frequency_GHz,
    o.observed_frequency_GHz,
    i.radial_velocity_km_s,
    i.fractional_abundance,
    i.thermal_release_screen,
    i.photochemical_screen
FROM spectral_observations o
JOIN astro_sources s ON o.source_id = s.source_id
JOIN molecular_species m ON o.species_id = m.species_id
LEFT JOIN astrochemical_indicators i ON o.observation_id = i.observation_id
ORDER BY s.environment, m.species_name;

-- Sample query 2: high photochemical processing records.
SELECT
    o.observation_id,
    s.source_name,
    s.environment,
    m.species_name,
    o.uv_field_index,
    i.photodissociation_lifetime_years_simplified
FROM spectral_observations o
JOIN astro_sources s ON o.source_id = s.source_id
JOIN molecular_species m ON o.species_id = m.species_id
JOIN astrochemical_indicators i ON o.observation_id = i.observation_id
WHERE i.photochemical_screen = 'high_photochemical_processing'
ORDER BY o.uv_field_index DESC;

-- Sample query 3: mean abundance by environment.
SELECT
    s.environment,
    COUNT(*) AS record_count,
    AVG(i.fractional_abundance) AS mean_fractional_abundance,
    AVG(o.dust_temperature_K) AS mean_dust_temperature_K,
    AVG(o.uv_field_index) AS mean_uv_field_index
FROM spectral_observations o
JOIN astro_sources s ON o.source_id = s.source_id
JOIN astrochemical_indicators i ON o.observation_id = i.observation_id
GROUP BY s.environment
ORDER BY mean_fractional_abundance DESC;
