-- Highest-reliability synthetic classifications.
SELECT
    r.sample_name,
    i.assigned_class,
    r.phase,
    r.functional_group,
    i.evidence_score,
    i.classification_reliability,
    i.hazard_triage
FROM chemical_classification_indicators i
JOIN chemical_records r ON i.record_id = r.record_id
ORDER BY i.classification_reliability DESC;

-- Classification summary.
SELECT
    i.assigned_class,
    COUNT(*) AS n,
    AVG(i.evidence_score) AS mean_evidence_score,
    AVG(i.classification_reliability) AS mean_reliability,
    AVG(r.hazard_indicator_score) AS mean_hazard_indicator_score
FROM chemical_classification_indicators i
JOIN chemical_records r ON i.record_id = r.record_id
GROUP BY i.assigned_class
ORDER BY mean_reliability DESC;
