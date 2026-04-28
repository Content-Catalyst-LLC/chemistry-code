.headers on
.mode column

SELECT
    case_id,
    reaction,
    K,
    ROUND((C_mol_l * CASE WHEN stoich_D > 0 THEN D_mol_l ELSE 1 END) / (A_mol_l * B_mol_l), 6) AS Q
FROM reaction_quotient_cases
ORDER BY case_id;

SELECT
    case_id,
    K,
    ROUND(total_concentration_mol_l / (1.0 + K), 6) AS A_eq_mol_l,
    ROUND(total_concentration_mol_l - total_concentration_mol_l / (1.0 + K), 6) AS B_eq_mol_l
FROM simple_equilibrium_cases
ORDER BY case_id;

SELECT
    reaction,
    temperature_K,
    K,
    ROUND(inverse_temperature_K_inv, 7) AS inverse_temperature,
    ROUND(ln_K, 6) AS ln_K
FROM vant_hoff_equilibrium
ORDER BY reaction, temperature_K;

SELECT
    case_id,
    salt,
    Ksp,
    cation_concentration_mol_l,
    anion_concentration_mol_l,
    (cation_concentration_mol_l * POWER(anion_concentration_mol_l, anion_power)) AS ion_product
FROM solubility_cases
ORDER BY case_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
