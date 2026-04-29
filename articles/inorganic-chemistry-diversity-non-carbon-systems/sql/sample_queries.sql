.headers on
.mode column

SELECT
    compound,
    unknown_element,
    ROUND((total_charge - known_contribution) / unknown_atom_count, 3) AS unknown_oxidation_state
FROM oxidation_state_cases
ORDER BY compound;

SELECT
    complex_id,
    formal_oxidation_state,
    coordination_number,
    geometry,
    charge
FROM coordination_cases
ORDER BY coordination_number DESC;

SELECT
    ligand,
    charge,
    donor_atoms,
    denticity,
    field_strength_hint
FROM ligand_cases
ORDER BY ligand;

SELECT
    case_id,
    d_electron_count,
    ROUND(t2g_electrons * -0.4 * delta_o_units + eg_electrons * 0.6 * delta_o_units, 3) AS CFSE_delta_o_units,
    ROUND(SQRT(unpaired_electrons * (unpaired_electrons + 2)), 3) AS spin_only_magnetic_moment_BM
FROM crystal_field_cases
ORDER BY case_id;

SELECT
    material,
    ROUND((r_A + r_X) / (SQRT(2) * (r_B + r_X)), 3) AS tolerance_factor
FROM perovskite_cases
ORDER BY material;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
