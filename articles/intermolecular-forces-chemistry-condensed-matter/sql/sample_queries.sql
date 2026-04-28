.headers on
.mode column

SELECT
    pair,
    epsilon_kj_mol,
    sigma_angstrom,
    interaction_note
FROM pair_potential_parameters
ORDER BY epsilon_kj_mol DESC;

SELECT
    substance,
    temperature_K,
    pressure_kPa,
    ROUND(inverse_temperature_K_inv, 6) AS inverse_temperature_K_inv
FROM vapor_pressure_measurements
ORDER BY temperature_K;

SELECT
    phase_at_room_conditions,
    COUNT(*) AS substance_count
FROM phase_properties
GROUP BY phase_at_room_conditions
ORDER BY phase_at_room_conditions;

SELECT
    dominant_interaction,
    AVG(surface_tension_mN_m) AS mean_surface_tension_mN_m,
    COUNT(*) AS liquid_count
FROM surface_tension_measurements
GROUP BY dominant_interaction
ORDER BY mean_surface_tension_mN_m DESC;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
