.mode column
.headers on

SELECT
    sample,
    substance,
    formula,
    ROUND(mass_g / molar_mass_g_mol, 6) AS moles,
    ROUND((mass_g / molar_mass_g_mol) / volume_l, 6) AS concentration_mol_l
FROM mass_volume_concentration;

SELECT
    solution,
    ROUND((target_concentration_mol_l * final_volume_ml) / stock_concentration_mol_l, 6) AS stock_volume_ml,
    ROUND(final_volume_ml - ((target_concentration_mol_l * final_volume_ml) / stock_concentration_mol_l), 6) AS diluent_volume_ml
FROM dilution_plan;

SELECT
    sample,
    COUNT(*) AS n_replicates,
    ROUND(AVG(measured_mass_g), 8) AS mean_mass_g
FROM replicate_measurements
GROUP BY sample;

SELECT
    record_id,
    sample,
    instrument,
    method,
    unit,
    standard_reference
FROM measurement_metadata
ORDER BY record_id;
