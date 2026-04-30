-- Query 1: highest attention toxicology records.
SELECT
    e.record_id,
    c.chemical_name,
    c.chemical_class,
    e.medium,
    e.route,
    e.target_system,
    i.hazard_quotient,
    i.vulnerability_adjusted_hazard,
    i.margin_of_exposure,
    i.cancer_risk_proxy,
    i.mc_probability_hq_above_1,
    i.attention_flag
FROM toxicology_indicators i
JOIN exposure_records e ON i.record_id = e.record_id
JOIN toxicology_chemicals c ON e.chemical_id = c.chemical_id
ORDER BY i.evidence_weighted_risk_index DESC;

-- Query 2: target-system hazard index.
SELECT
    e.target_system,
    COUNT(*) AS n,
    SUM(i.hazard_quotient) AS hazard_index,
    SUM(i.vulnerability_adjusted_hazard) AS vulnerability_adjusted_hazard_index,
    MAX(i.cancer_risk_proxy) AS max_cancer_risk_proxy
FROM toxicology_indicators i
JOIN exposure_records e ON i.record_id = e.record_id
GROUP BY e.target_system
ORDER BY vulnerability_adjusted_hazard_index DESC;

-- Query 3: mixture group hazard index.
SELECT
    c.mixture_group,
    COUNT(*) AS n,
    SUM(i.hazard_quotient) AS hazard_index,
    SUM(i.vulnerability_adjusted_hazard) AS vulnerability_adjusted_hazard_index
FROM toxicology_indicators i
JOIN exposure_records e ON i.record_id = e.record_id
JOIN toxicology_chemicals c ON e.chemical_id = c.chemical_id
GROUP BY c.mixture_group
ORDER BY vulnerability_adjusted_hazard_index DESC;

-- Query 4: scenario outputs.
SELECT
    scenario_type,
    scenario_name,
    variable_name,
    variable_value,
    variable_unit
FROM toxicology_scenario_outputs
ORDER BY scenario_type, scenario_name, variable_name;
