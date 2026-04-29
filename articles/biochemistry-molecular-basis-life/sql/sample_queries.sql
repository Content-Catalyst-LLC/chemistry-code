.headers on
.mode column

SELECT
    case_id,
    substrate_mM,
    ROUND(Vmax_units * substrate_mM / (Km_mM + substrate_mM), 6) AS velocity_units
FROM enzyme_kinetics_cases
ORDER BY substrate_mM;

SELECT
    case_id,
    ligand_uM,
    ROUND(ligand_uM / (Kd_uM + ligand_uM), 6) AS fractional_occupancy
FROM binding_cases
ORDER BY ligand_uM;

SELECT
    biomolecule_class,
    monomer_or_unit,
    polymer_or_assembly,
    major_functions
FROM biomolecule_classes
ORDER BY biomolecule_class;

SELECT
    case_id,
    ROUND(-(8.314462618 * temperature_K * LN(equilibrium_constant)) / 1000.0, 6) AS delta_g_standard_kj_mol
FROM energy_cases
ORDER BY case_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
