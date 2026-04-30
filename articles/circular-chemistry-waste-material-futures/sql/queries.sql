-- Highest-scoring synthetic circular material streams.
SELECT
    s.material_stream,
    s.material_class,
    s.recovery_pathway,
    i.recovery_yield,
    i.circular_retention,
    i.safe_circularity_score,
    i.circular_chemistry_score,
    i.profile_flag
FROM circular_chemistry_indicators i
JOIN circular_material_streams s ON i.stream_id = s.stream_id
ORDER BY i.circular_chemistry_score DESC;

-- Material-class summary.
SELECT
    s.material_class,
    COUNT(*) AS n,
    AVG(i.recovery_yield) AS mean_recovery_yield,
    AVG(i.circular_retention) AS mean_circular_retention,
    AVG(i.safe_circularity_score) AS mean_safe_circularity,
    AVG(i.circular_chemistry_score) AS mean_circular_score
FROM circular_chemistry_indicators i
JOIN circular_material_streams s ON i.stream_id = s.stream_id
GROUP BY s.material_class
ORDER BY mean_circular_score DESC;
