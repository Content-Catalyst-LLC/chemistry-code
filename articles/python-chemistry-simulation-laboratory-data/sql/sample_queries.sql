.headers on
.mode column

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
    sample_id,
    method_id,
    ROUND(AVG(measurement_mM), 6) AS mean_mM,
    COUNT(*) AS n
FROM replicate_measurements
GROUP BY sample_id, method_id
ORDER BY sample_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
