.headers on
.mode column

SELECT
    experiment,
    process,
    ROUND(solution_mass_g * specific_heat_j_g_k * temperature_change_k, 3) AS q_solution_j,
    ROUND(-1.0 * (
        solution_mass_g * specific_heat_j_g_k * temperature_change_k +
        calorimeter_heat_capacity_j_k * temperature_change_k
    ), 3) AS q_reaction_j
FROM calorimetry_examples
ORDER BY experiment;

SELECT
    reaction_id,
    ROUND(SUM(coefficient * delta_h_f_kj_mol), 3) AS delta_h_reaction_kj_mol
FROM formation_enthalpy_examples
GROUP BY reaction_id
ORDER BY reaction_id;

SELECT
    reaction,
    ROUND(delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0, 3) AS delta_g_standard_kj_mol,
    ROUND(EXP(-((delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0) * 1000.0) / (8.314462618 * temperature_k)), 6) AS equilibrium_constant
FROM gibbs_examples
ORDER BY reaction;

SELECT
    coupling_case,
    ROUND(SUM(delta_g_kj_mol), 3) AS total_delta_g_kj_mol,
    COUNT(*) AS step_count
FROM coupled_reaction_examples
GROUP BY coupling_case
ORDER BY coupling_case;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
