.headers on
.mode column

SELECT
    standard_id,
    concentration_mg_L,
    signal
FROM calibration_standards
ORDER BY concentration_mg_L;

SELECT
    sample_id,
    ROUND(AVG(measured_mg_L), 4) AS mean_mg_L,
    ROUND(
        SQRT(
            (SUM(measured_mg_L * measured_mg_L) - COUNT(*) * AVG(measured_mg_L) * AVG(measured_mg_L))
            / (COUNT(*) - 1)
        ),
        4
    ) AS sd_mg_L
FROM replicate_measurements
GROUP BY sample_id;

SELECT
    sample_id,
    ROUND(100 * (spiked_mg_L - unspiked_mg_L) / spike_added_mg_L, 3) AS recovery_percent
FROM spike_recovery
ORDER BY sample_id;

SELECT
    pair,
    ROUND(2 * (tR_2_min - tR_1_min) / (w1_min + w2_min), 3) AS resolution
FROM chromatography_peaks
ORDER BY pair;

SELECT
    case_id,
    ROUND(absorbance / (epsilon_L_mol_cm * path_length_cm), 10) AS concentration_mol_L
FROM beer_lambert_cases
ORDER BY case_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
