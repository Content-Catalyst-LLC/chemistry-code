.headers on
.mode column

SELECT
    period,
    block,
    category,
    COUNT(*) AS element_count
FROM elements
GROUP BY period, block, category
ORDER BY period, block, category;

SELECT
    element_symbol,
    ROUND(SUM(isotopic_mass_u * fractional_abundance), 6) AS weighted_atomic_mass_u,
    ROUND(SUM(fractional_abundance), 6) AS abundance_sum,
    COUNT(*) AS isotope_count
FROM isotopes
GROUP BY element_symbol
ORDER BY element_symbol;

SELECT
    isotope,
    atomic_number,
    mass_number,
    neutron_number
FROM isotopes
ORDER BY element_symbol, mass_number;

SELECT
    sample,
    entity,
    mass_g,
    molar_mass_g_mol,
    amount_mol,
    amount_mol * 6.02214076e23 AS estimated_entities
FROM mole_examples
ORDER BY sample;

SELECT
    compound,
    formula,
    element_symbol,
    atom_count,
    atomic_mass_u,
    ROUND(
        element_mass_contribution /
        SUM(element_mass_contribution) OVER (PARTITION BY compound) * 100,
        4
    ) AS percent_by_mass
FROM compounds
ORDER BY compound, element_symbol;
