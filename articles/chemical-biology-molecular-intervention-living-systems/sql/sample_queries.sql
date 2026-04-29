.headers on
.mode column

SELECT
    case_id,
    compound_uM,
    ROUND(bottom + (top - bottom) / (1 + POWER(EC50_uM / compound_uM, hill_slope)), 6) AS response_fraction
FROM dose_response_cases
ORDER BY compound_uM;

SELECT
    case_id,
    ligand_uM,
    ROUND(ligand_uM / (Kd_uM + ligand_uM), 6) AS fractional_occupancy
FROM occupancy_cases
ORDER BY ligand_uM;

SELECT
    condition,
    ROUND((signal_control - signal_treated) / (signal_control - signal_max), 6) AS target_engagement_fraction
FROM target_engagement_cases
ORDER BY compound_uM;

SELECT
    probe,
    ROUND(off_target_potency_nM / target_potency_nM, 3) AS selectivity_ratio,
    cellular_target_engagement,
    inactive_control_available
FROM probe_quality_cases
ORDER BY selectivity_ratio DESC;

SELECT
    feature,
    ROUND(treated - control, 3) AS delta
FROM perturbation_features
ORDER BY ABS(treated - control) DESC;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
