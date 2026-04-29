.headers on
.mode column

SELECT
    species_id,
    reaction_id,
    coefficient
FROM stoichiometry
ORDER BY species_id, reaction_id;

SELECT
    case_id,
    ROUND(k_to_B / (k_to_B + k_to_C), 6) AS fraction_to_B,
    ROUND(k_to_C / (k_to_B + k_to_C), 6) AS fraction_to_C,
    ROUND(k_to_B / k_to_C, 6) AS B_to_C_selectivity
FROM parallel_cases
ORDER BY case_id;

SELECT
    reaction_id,
    reaction,
    rate_constant,
    description
FROM reactions
ORDER BY reaction_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
