.headers on
.mode column

SELECT
    molecule,
    heavy_atoms,
    hetero_atoms,
    ROUND(CAST(hetero_atoms AS REAL) / heavy_atoms, 3) AS hetero_atom_fraction,
    h_bond_donors + h_bond_acceptors AS polarity_score
FROM molecular_descriptors
ORDER BY molecule;

SELECT
    molecule,
    conformer,
    relative_energy_kj_mol,
    ROUND(EXP(-(relative_energy_kj_mol * 1000.0) / (8.314462618 * temperature_K)), 6) AS boltzmann_weight
FROM conformer_energies
ORDER BY molecule, relative_energy_kj_mol;

SELECT
    case_id,
    distance,
    ROUND(4 * epsilon * (POWER(sigma / distance, 12) - POWER(sigma / distance, 6)), 6) AS lj_energy
FROM lennard_jones_cases
ORDER BY distance;

SELECT
    reaction,
    product_energy_kj_mol - reactant_energy_kj_mol AS reaction_energy_kj_mol,
    transition_state_energy_kj_mol - reactant_energy_kj_mol AS activation_energy_kj_mol
FROM reaction_energies
ORDER BY reaction;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
