-- Highest-priority synthetic compounds.
SELECT
    c.compound_id,
    c.project,
    c.target,
    d.pIC50,
    d.selectivity_window,
    d.lipophilic_ligand_efficiency,
    d.safety_liability_score,
    d.multiparameter_optimization_score,
    d.advancement_recommendation
FROM decision_indicators d
JOIN compounds c ON d.compound_id = c.compound_id
ORDER BY d.multiparameter_optimization_score DESC;

-- Safety-liability review queue.
SELECT
    c.compound_id,
    c.project,
    a.hERG_ic50_uM,
    a.cyp3a4_ic50_uM,
    c.alert_count,
    d.safety_liability_score,
    d.advancement_recommendation
FROM decision_indicators d
JOIN compounds c ON d.compound_id = c.compound_id
JOIN admet_results a ON c.compound_id = a.compound_id
WHERE d.safety_liability_score >= 0.50
ORDER BY d.safety_liability_score DESC;
