.headers on
.mode column

SELECT
    sample_id,
    analyte,
    ROUND(AVG(measurement_mM), 6) AS mean_mM,
    COUNT(*) AS n
FROM replicate_measurements
GROUP BY sample_id, analyte
ORDER BY sample_id;

SELECT
    concentration_mM,
    ROUND(AVG(response), 6) AS mean_response,
    COUNT(*) AS n
FROM calibration_standards
GROUP BY concentration_mM
ORDER BY concentration_mM;

SELECT
    sample_id,
    ROUND(AVG(response), 6) AS mean_response,
    COUNT(*) AS n
FROM unknown_samples
GROUP BY sample_id
ORDER BY sample_id;

SELECT
    time_s,
    concentration_mM,
    ROUND(LOG(concentration_mM), 6) AS ln_concentration
FROM kinetics_timeseries
ORDER BY time_s;

SELECT
    temperature_K,
    rate_constant_s_inv,
    ROUND(1.0 / temperature_K, 8) AS inverse_temperature,
    ROUND(LOG(rate_constant_s_inv), 6) AS ln_rate_constant
FROM arrhenius_rates
ORDER BY temperature_K;

SELECT
    temperature_level,
    catalyst_loading,
    solvent,
    ROUND(AVG(yield_percent), 3) AS mean_yield_percent
FROM experimental_design
GROUP BY temperature_level, catalyst_loading, solvent
ORDER BY solvent, temperature_level, catalyst_loading;

SELECT
    control_type,
    ROUND(AVG(100.0 * measured_mM / expected_mM), 3) AS mean_recovery_percent,
    COUNT(*) AS n
FROM qc_samples
GROUP BY control_type
ORDER BY control_type;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
