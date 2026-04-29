.headers on
.mode column

SELECT
    particle,
    position,
    velocity,
    force / mass AS acceleration,
    position + velocity * 0.5 + 0.5 * (force / mass) * 0.5 * 0.5 AS new_position,
    velocity + (force / mass) * 0.5 AS new_velocity
FROM particles_initial
ORDER BY particle;

SELECT
    case_id,
    distance,
    ROUND(4 * epsilon * (POWER(sigma / distance, 12) - POWER(sigma / distance, 6)), 6) AS lj_energy
FROM lennard_jones_cases
ORDER BY distance;

SELECT
    case_id,
    ROUND(138.935456 * charge_i * charge_j / (dielectric * distance), 6) AS coulomb_energy
FROM coulomb_cases
ORDER BY case_id;

SELECT
    time_ps,
    ROUND((x - (SELECT x FROM trajectory_positions WHERE time_ps = 0)) * (x - (SELECT x FROM trajectory_positions WHERE time_ps = 0)) +
          (y - (SELECT y FROM trajectory_positions WHERE time_ps = 0)) * (y - (SELECT y FROM trajectory_positions WHERE time_ps = 0)) +
          (z - (SELECT z FROM trajectory_positions WHERE time_ps = 0)) * (z - (SELECT z FROM trajectory_positions WHERE time_ps = 0)), 6) AS msd
FROM trajectory_positions
ORDER BY time_ps;

SELECT
    protocol_id,
    ensemble,
    temperature_K,
    timestep_fs,
    production_ns,
    thermostat,
    barostat
FROM ensemble_protocols
ORDER BY protocol_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
