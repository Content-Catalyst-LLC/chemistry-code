-- Query 1: highest atmospheric chemistry pressure records.
SELECT
    o.observation_id,
    s.station_name,
    s.region,
    s.environment,
    o.species,
    o.chemical_class,
    o.concentration,
    o.reference_concentration,
    o.unit,
    i.reference_ratio,
    i.greenhouse_forcing_proxy_W_m2,
    i.photochemical_ozone_index,
    i.aerosol_pressure_index,
    i.atmospheric_chemistry_pressure_index,
    i.attention_flag
FROM atmospheric_advanced_indicators i
JOIN atmospheric_observations o ON i.observation_id = o.observation_id
JOIN atmospheric_stations s ON o.station_id = s.station_id
ORDER BY i.atmospheric_chemistry_pressure_index DESC;

-- Query 2: greenhouse gas forcing proxies.
SELECT
    o.species,
    o.concentration,
    o.reference_concentration,
    o.unit,
    i.greenhouse_forcing_proxy_W_m2,
    i.lifetime_persistence_factor,
    i.atmospheric_chemistry_pressure_index
FROM atmospheric_advanced_indicators i
JOIN atmospheric_observations o ON i.observation_id = o.observation_id
WHERE o.chemical_class = 'greenhouse_gas'
ORDER BY i.greenhouse_forcing_proxy_W_m2 DESC;

-- Query 3: photochemical ozone potential screens.
SELECT
    s.station_name,
    o.species,
    c.nox_ppb,
    c.voc_ppb,
    c.sunlight_index,
    i.photochemical_ozone_index,
    i.attention_flag
FROM atmospheric_advanced_indicators i
JOIN atmospheric_observations o ON i.observation_id = o.observation_id
JOIN atmospheric_stations s ON o.station_id = s.station_id
JOIN atmospheric_context c ON o.observation_id = c.observation_id
WHERE i.photochemical_ozone_index > 40
ORDER BY i.photochemical_ozone_index DESC;

-- Query 4: scenario outputs.
SELECT
    scenario_type,
    scenario_name,
    time_step,
    variable_name,
    variable_value,
    variable_unit
FROM atmospheric_scenario_outputs
ORDER BY scenario_type, scenario_name, time_step;
