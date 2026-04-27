.mode column
.headers on

SELECT
    reaction,
    reactant_mass_g,
    product_mass_g,
    ROUND(product_mass_g - reactant_mass_g, 5) AS mass_difference_g,
    system_type
FROM mass_conservation_examples;

SELECT
    metal,
    oxide_name,
    ROUND(metal_mass_g + oxygen_mass_g, 5) AS oxide_mass_g,
    ROUND(oxygen_mass_g / (metal_mass_g + oxygen_mass_g), 5) AS oxygen_mass_fraction,
    ROUND(100.0 * oxygen_mass_g / metal_mass_g, 5) AS mass_gain_percent
FROM oxidation_mass_gain;

SELECT
    reaction,
    carbon_moles,
    oxygen_moles_required,
    carbon_dioxide_moles_produced
FROM combustion_stoichiometry;

SELECT
    older_name,
    modern_name,
    conceptual_shift
FROM nomenclature_mapping
ORDER BY conceptual_shift, older_name;
