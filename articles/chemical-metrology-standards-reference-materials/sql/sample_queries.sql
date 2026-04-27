.mode column
.headers on

SELECT
    component,
    standard_uncertainty,
    ROUND(standard_uncertainty * standard_uncertainty, 8) AS variance_contribution,
    category
FROM uncertainty_budget
ORDER BY variance_contribution DESC;

SELECT
    material_id,
    material_type,
    measurand,
    certified_value,
    expanded_uncertainty,
    unit,
    ROUND(100.0 * expanded_uncertainty / ABS(certified_value), 4) AS relative_uncertainty_percent
FROM reference_materials;

SELECT
    step_order,
    chain_level,
    reference,
    expanded_uncertainty,
    unit
FROM traceability_chain
ORDER BY step_order;

SELECT
    laboratory,
    lab_result,
    lab_result - reference_value AS bias,
    ROUND(
        (lab_result - reference_value) /
        SQRT(lab_expanded_uncertainty * lab_expanded_uncertainty + reference_expanded_uncertainty * reference_expanded_uncertainty),
        4
    ) AS normalized_error_en
FROM interlaboratory_comparison;
