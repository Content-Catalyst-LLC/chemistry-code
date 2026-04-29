.headers on
.mode column

SELECT
    case_id,
    delta_g_standard_kj_mol,
    ROUND(EXP(-(delta_g_standard_kj_mol * 1000.0) / (8.314462618 * temperature_K)), 6) AS K
FROM thermodynamic_cases
ORDER BY case_id;

SELECT
    case_id,
    temperature_K,
    ROUND(pre_exponential_s_inv * EXP(-(activation_energy_kj_mol * 1000.0) / (8.314462618 * temperature_K)), 6) AS rate_constant_s_inv
FROM arrhenius_cases
ORDER BY temperature_K;

SELECT
    case_id,
    ROUND(E_standard_V - (8.314462618 * temperature_K / (electrons_transferred * 96485.33212)) * LN(reaction_quotient), 6) AS E_V
FROM electrochemistry_cases
ORDER BY case_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
