-- Query 1: highest-priority candidates by multiparameter score.
SELECT
    c.compound_id,
    p.project_name,
    p.target,
    p.target_class,
    i.pIC50,
    i.selectivity_window,
    i.lipophilic_ligand_efficiency,
    i.oral_property_score,
    i.safety_liability_score,
    i.developability_score,
    i.multiparameter_optimization_score,
    i.mc_advancement_probability,
    i.advancement_recommendation
FROM medicinal_advanced_indicators i
JOIN compounds c ON i.compound_id = c.compound_id
JOIN discovery_projects p ON c.project_id = p.project_id
ORDER BY i.multiparameter_optimization_score DESC;

-- Query 2: safety-liability review queue.
SELECT
    c.compound_id,
    p.project_name,
    a.hERG_ic50_uM,
    a.cyp3a4_ic50_uM,
    c.alert_count,
    i.safety_liability_score,
    i.advancement_recommendation
FROM medicinal_advanced_indicators i
JOIN compounds c ON i.compound_id = c.compound_id
JOIN discovery_projects p ON c.project_id = p.project_id
JOIN admet_results a ON c.compound_id = a.compound_id
WHERE i.safety_liability_score >= 0.50
ORDER BY i.safety_liability_score DESC;

-- Query 3: project-level discovery summaries.
SELECT
    p.project_name,
    p.target,
    p.target_class,
    COUNT(*) AS compound_count,
    AVG(i.pIC50) AS mean_pIC50,
    MAX(i.pIC50) AS best_pIC50,
    AVG(i.lipophilic_ligand_efficiency) AS mean_LLE,
    AVG(i.developability_score) AS mean_developability,
    AVG(i.multiparameter_optimization_score) AS mean_MPO,
    SUM(CASE WHEN i.advancement_recommendation = 'advance_to_integrated_profiling' THEN 1 ELSE 0 END) AS advance_count
FROM medicinal_advanced_indicators i
JOIN compounds c ON i.compound_id = c.compound_id
JOIN discovery_projects p ON c.project_id = p.project_id
GROUP BY p.project_name, p.target, p.target_class
ORDER BY mean_MPO DESC;

-- Query 4: scenario outputs.
SELECT
    compound_id,
    scenario_type,
    scenario_name,
    variable_name,
    variable_value,
    variable_unit
FROM medicinal_scenario_outputs
ORDER BY scenario_type, compound_id, variable_name;
