-- Query 1: highest nutrition chemistry quality profiles.
SELECT
    f.food_name,
    f.food_group,
    f.processing_level,
    i.nutrient_density_score,
    i.food_matrix_protection_index,
    i.glycemic_accessibility_proxy,
    i.lipid_oxidation_vulnerability,
    i.chemical_safety_attention_index,
    i.nutrition_chemistry_quality_index,
    i.profile_flag
FROM food_chemistry_indicators i
JOIN foods f ON i.food_id = f.food_id
ORDER BY i.nutrition_chemistry_quality_index DESC;

-- Query 2: food group summary.
SELECT
    f.food_group,
    COUNT(*) AS n,
    AVG(i.nutrient_density_score) AS mean_nutrient_density,
    AVG(i.food_matrix_protection_index) AS mean_matrix_protection,
    AVG(i.glycemic_accessibility_proxy) AS mean_glycemic_accessibility,
    AVG(i.lipid_oxidation_vulnerability) AS mean_lipid_oxidation_vulnerability,
    AVG(i.nutrition_chemistry_quality_index) AS mean_quality_index
FROM food_chemistry_indicators i
JOIN foods f ON i.food_id = f.food_id
GROUP BY f.food_group
ORDER BY mean_quality_index DESC;

-- Query 3: safety-context review queue.
SELECT
    f.food_name,
    f.food_group,
    i.chemical_safety_attention_index,
    i.profile_flag
FROM food_chemistry_indicators i
JOIN foods f ON i.food_id = f.food_id
WHERE i.chemical_safety_attention_index >= 0.50
ORDER BY i.chemical_safety_attention_index DESC;

-- Query 4: scenario outputs.
SELECT
    scenario_type,
    scenario_name,
    variable_name,
    variable_value,
    variable_unit
FROM food_chemistry_scenario_outputs
ORDER BY scenario_type, scenario_name, variable_name;
