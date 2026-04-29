.headers on
.mode column

SELECT
    case_id,
    temperature_K,
    delta_Ea_kJ_mol,
    ROUND(EXP((delta_Ea_kJ_mol * 1000.0) / (8.314462618 * temperature_K)), 3) AS rate_enhancement_estimate
FROM barrier_cases
ORDER BY case_id;

SELECT
    experiment,
    catalyst_type,
    ROUND(product_mol / catalyst_mol, 3) AS TON,
    ROUND((product_mol / catalyst_mol) / time_s, 8) AS TOF_s_inv,
    ROUND(product_mol / time_s, 10) AS catalytic_activity_mol_s
FROM turnover_experiments
ORDER BY experiment;

SELECT
    case_id,
    pressure,
    ROUND((K_A * pressure) / (1 + K_A * pressure), 6) AS theta_A,
    ROUND((K_B * pressure) / (1 + K_B * pressure), 6) AS theta_B
FROM adsorption_cases
ORDER BY pressure;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
