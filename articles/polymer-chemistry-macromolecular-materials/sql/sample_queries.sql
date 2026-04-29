-- Sample queries for synthetic polymer chemistry workflows.

-- 1. Flexible barrier candidates.
SELECT
    polymer_id,
    polymer_class,
    oxygen_permeability_relative,
    elongation_percent,
    recyclability_score
FROM polymer_candidate
WHERE oxygen_permeability_relative <= 0.35
  AND elongation_percent >= 100
ORDER BY oxygen_permeability_relative ASC;

-- 2. High-temperature processing review.
SELECT
    p.process_id,
    p.polymer_id,
    c.polymer_class,
    p.polymerization_route,
    p.processing_method,
    p.processing_temperature_C
FROM processing_condition p
JOIN polymer_candidate c
    ON p.polymer_id = c.polymer_id
WHERE p.processing_temperature_C >= 300
ORDER BY p.processing_temperature_C DESC;

-- 3. Degradation and lifecycle review flags.
SELECT
    l.polymer_id,
    c.polymer_class,
    l.hydrolysis_sensitive,
    l.oxidation_sensitive,
    l.uv_sensitive,
    l.recycling_pathway,
    l.biodegradation_claim_status
FROM degradation_lifecycle_note l
JOIN polymer_candidate c
    ON l.polymer_id = c.polymer_id
WHERE l.biodegradation_claim_status LIKE 'conditional%'
   OR l.recycling_pathway IN ('specialized_recycling', 'difficult_network_recycling')
ORDER BY l.polymer_id;

-- 4. Property measurements by polymer.
SELECT
    polymer_id,
    property_name,
    value,
    unit,
    method,
    temperature_C
FROM property_measurement
ORDER BY polymer_id, property_name;

-- 5. Molar-mass fractions for a selected polymer.
SELECT
    polymer_id,
    fraction_id,
    molecule_count,
    molar_mass_g_mol
FROM molar_mass_fraction
WHERE polymer_id = 'poly_A'
ORDER BY molar_mass_g_mol;
