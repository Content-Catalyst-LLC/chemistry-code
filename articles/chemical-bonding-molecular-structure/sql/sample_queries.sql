.headers on
.mode column

SELECT
    bond,
    atom_a,
    atom_b,
    ROUND(delta_chi, 3) AS delta_chi
FROM bond_polarity
ORDER BY delta_chi DESC;

SELECT
    species,
    atom,
    valence_electrons,
    nonbonding_electrons,
    bonding_electrons,
    formal_charge
FROM formal_charge_examples
ORDER BY species;

SELECT
    molecule,
    bonding_electrons,
    antibonding_electrons,
    bond_order
FROM mo_bond_order_examples
ORDER BY bond_order DESC;

SELECT
    molecule,
    central_atom,
    bonding_domains,
    lone_pair_domains,
    electron_domain_geometry,
    molecular_geometry
FROM vsepr_examples
ORDER BY bonding_domains + lone_pair_domains, molecule;

SELECT
    molecule,
    SUM(partial_charge * x_angstrom) AS dipole_x_e_angstrom,
    SUM(partial_charge * y_angstrom) AS dipole_y_e_angstrom,
    SUM(partial_charge * z_angstrom) AS dipole_z_e_angstrom
FROM molecular_coordinates
GROUP BY molecule
ORDER BY molecule;
