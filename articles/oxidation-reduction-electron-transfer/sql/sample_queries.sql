.headers on
.mode column

SELECT
    case_id,
    cell,
    ROUND(E_cathode_V - E_anode_V, 6) AS E_cell_standard_V,
    ROUND(-electrons_transferred * 96485.33212 * (E_cathode_V - E_anode_V) / 1000.0, 3) AS delta_g_standard_kj_mol
FROM cell_potential_cases
ORDER BY case_id;

SELECT
    case_id,
    E_standard_V,
    reaction_quotient,
    ROUND(E_standard_V - (8.314462618 * temperature_K / (electrons_transferred * 96485.33212)) * LN(reaction_quotient), 6) AS E_V
FROM nernst_cases
ORDER BY case_id;

SELECT
    case_id,
    ROUND((analyte_moles * electrons_donated_per_analyte) / electrons_accepted_per_titrant, 8) AS titrant_moles_required,
    ROUND(((analyte_moles * electrons_donated_per_analyte) / electrons_accepted_per_titrant) / titrant_concentration_mol_l * 1000, 3) AS titrant_volume_ml
FROM redox_titration_cases
ORDER BY case_id;

SELECT
    case_id,
    metal_a,
    E_reduction_a_V,
    metal_b,
    E_reduction_b_V
FROM corrosion_pairs
ORDER BY case_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
