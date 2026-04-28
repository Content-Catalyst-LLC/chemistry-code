.headers on
.mode column

SELECT
    subshell,
    l,
    orbital_count,
    maximum_electrons
FROM orbitals
ORDER BY l;

SELECT
    symbol,
    name,
    atomic_number,
    configuration,
    valence_electrons,
    block
FROM electron_configurations
ORDER BY atomic_number;

SELECT
    symbol,
    atomic_number,
    shielding_constant,
    effective_nuclear_charge
FROM effective_nuclear_charge
ORDER BY atomic_number;

SELECT
    'n=' || n.value AS level,
    ROUND(-13.6 / (n.value * n.value), 6) AS energy_eV
FROM (
    SELECT 1 AS value UNION ALL SELECT 2 UNION ALL SELECT 3
    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
) AS n;

SELECT
    matrix_name,
    h11,
    h22,
    h33
FROM hamiltonian_matrices
ORDER BY matrix_name;
