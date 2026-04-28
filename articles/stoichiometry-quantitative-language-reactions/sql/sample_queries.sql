.headers on
.mode column

SELECT
    e.case_id,
    r.equation,
    ROUND(e.available_a_mol / r.coefficient_a, 6) AS extent_from_a,
    ROUND(
        CASE
            WHEN r.coefficient_b > 0 THEN e.available_b_mol / r.coefficient_b
            ELSE NULL
        END,
        6
    ) AS extent_from_b
FROM limiting_reagent_examples e
JOIN reactions r ON e.reaction_id = r.reaction_id
ORDER BY e.case_id;

SELECT
    case_id,
    ROUND((target_concentration_mol_l * target_volume_l) / stock_concentration_mol_l, 6) AS stock_volume_l,
    ROUND(1000.0 * (target_concentration_mol_l * target_volume_l) / stock_concentration_mol_l, 3) AS stock_volume_ml
FROM solution_examples
ORDER BY case_id;

SELECT
    case_id,
    analyte_name,
    titrant_name,
    ROUND(
        analyte_coefficient * titrant_concentration_mol_l * titrant_volume_l /
        (titrant_coefficient * analyte_volume_l),
        6
    ) AS analyte_concentration_mol_l
FROM titration_examples
ORDER BY case_id;

SELECT
    case_id,
    species,
    initial_mol,
    stoichiometric_number,
    extent_mol,
    final_mol
FROM reaction_extent_examples
ORDER BY case_id, species;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
