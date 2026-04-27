.mode column
.headers on

SELECT
    substance,
    formula,
    ROUND(mass_g / molar_mass_g_mol, 5) AS moles,
    ROUND((mass_g / molar_mass_g_mol) / volume_l, 5) AS molarity_mol_l
FROM substances;

SELECT
    solution,
    ROUND(-LOG(hydrogen_concentration_mol_l) / LOG(10), 4) AS pH
FROM ph_examples
ORDER BY pH;

SELECT
    reaction,
    initial_concentration_mol_l,
    rate_constant_per_min,
    total_time_min
FROM kinetics_examples;

SELECT
    COUNT(*) AS n_calibration_points,
    MIN(concentration_mol_l) AS min_concentration,
    MAX(concentration_mol_l) AS max_concentration
FROM beer_lambert_calibration;
