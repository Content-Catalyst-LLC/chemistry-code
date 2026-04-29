.headers on
.mode column

SELECT
    case_id,
    energy_a,
    energy_b,
    coupling,
    ROUND((energy_a + energy_b - SQRT((energy_a - energy_b) * (energy_a - energy_b) + 4 * coupling * coupling)) / 2, 6) AS lower_energy,
    ROUND((energy_a + energy_b + SQRT((energy_a - energy_b) * (energy_a - energy_b) + 4 * coupling * coupling)) / 2, 6) AS upper_energy
FROM orbital_mixing_cases
ORDER BY case_id;

SELECT
    grid_point,
    x,
    ROUND(occupancy_1 * orbital_1 * orbital_1 + occupancy_2 * orbital_2 * orbital_2, 6) AS density
FROM electron_density_grid
ORDER BY x;

SELECT
    case_id,
    basis,
    energy_hartree,
    basis_size
FROM basis_convergence
ORDER BY case_id, basis_size;

SELECT
    complex,
    spin_state,
    multiplicity,
    relative_energy_kj_mol
FROM spin_state_cases
ORDER BY complex, relative_energy_kj_mol;

SELECT
    reaction,
    activation_free_energy_kj_mol,
    ROUND(LOG10((1.380649e-23 * temperature_K / 6.62607015e-34) * EXP(-(activation_free_energy_kj_mol * 1000.0) / (8.314462618 * temperature_K))), 6) AS log10_rate
FROM tst_cases
ORDER BY activation_free_energy_kj_mol;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
