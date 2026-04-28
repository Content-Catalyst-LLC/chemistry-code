.headers on
.mode column

SELECT
    experiment,
    time_min,
    concentration_mol_l,
    ROUND(ln_concentration, 6) AS ln_concentration
FROM first_order_data
ORDER BY experiment, time_min;

SELECT
    reaction,
    temperature_K,
    rate_constant_s_inv,
    ROUND(inverse_temperature_K_inv, 7) AS inverse_temperature_K_inv,
    ROUND(ln_k, 6) AS ln_k
FROM arrhenius_data
ORDER BY reaction, temperature_K;

SELECT
    experiment,
    substrate_mM,
    rate_umol_min,
    ROUND(inverse_substrate, 6) AS inverse_substrate,
    ROUND(inverse_rate, 6) AS inverse_rate
FROM enzyme_kinetics_data
ORDER BY substrate_mM;

SELECT
    mechanism,
    k1_per_min,
    k2_per_min,
    A0_mol_l,
    B0_mol_l,
    C0_mol_l
FROM mechanism_parameters
ORDER BY mechanism;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
