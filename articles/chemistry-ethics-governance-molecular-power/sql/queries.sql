-- Highest governance-gap synthetic records.
SELECT
    r.chemical_domain,
    r.use_context,
    i.chemical_risk,
    i.justice_weighted_risk,
    i.governance_gap,
    i.governance_flag
FROM molecular_power_indicators i
JOIN molecular_power_records r ON i.record_id = r.record_id
ORDER BY i.governance_gap DESC;

-- Domain summary.
SELECT
    r.chemical_domain,
    COUNT(*) AS n,
    AVG(r.benefit_score) AS mean_benefit,
    AVG(i.chemical_risk) AS mean_risk,
    AVG(i.justice_weighted_risk) AS mean_justice_risk,
    AVG(i.governance_gap) AS mean_governance_gap,
    AVG(i.responsible_innovation_score) AS mean_responsible_score
FROM molecular_power_indicators i
JOIN molecular_power_records r ON i.record_id = r.record_id
GROUP BY r.chemical_domain
ORDER BY mean_governance_gap DESC;
