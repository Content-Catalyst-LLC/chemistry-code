.headers on
.mode column

SELECT
    block,
    COUNT(*) AS element_count
FROM elements
GROUP BY block
ORDER BY block;

SELECT
    family,
    COUNT(*) AS element_count
FROM elements
GROUP BY family
ORDER BY element_count DESC, family;

SELECT
    period,
    block,
    COUNT(*) AS element_count
FROM elements
GROUP BY period, block
ORDER BY period, block;

SELECT
    element_symbol,
    ROUND(SUM(weighted_contribution_u), 6) AS weighted_atomic_mass_u,
    ROUND(SUM(fractional_abundance), 6) AS abundance_sum,
    COUNT(*) AS isotope_count
FROM isotopes
GROUP BY element_symbol
ORDER BY element_symbol;

SELECT
    symbol,
    name,
    atomic_number,
    "group",
    period,
    block,
    category,
    family
FROM elements
ORDER BY atomic_number;

SELECT
    classification_layer,
    description
FROM classification_rules
ORDER BY rule_id;
