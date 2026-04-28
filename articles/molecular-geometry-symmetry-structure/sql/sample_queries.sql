.headers on
.mode column

SELECT
    b.molecule,
    b.atom_i,
    b.atom_j,
    b.bond_type,
    ROUND(
        sqrt(
            (a.x_angstrom - c.x_angstrom) * (a.x_angstrom - c.x_angstrom) +
            (a.y_angstrom - c.y_angstrom) * (a.y_angstrom - c.y_angstrom) +
            (a.z_angstrom - c.z_angstrom) * (a.z_angstrom - c.z_angstrom)
        ),
        4
    ) AS distance_angstrom
FROM bonds b
JOIN molecular_coordinates a
  ON b.molecule = a.molecule AND b.atom_i = a.atom
JOIN molecular_coordinates c
  ON b.molecule = c.molecule AND b.atom_j = c.atom
ORDER BY b.molecule, b.atom_i, b.atom_j;

SELECT
    molecule,
    central_atom,
    bonding_domains,
    lone_pair_domains,
    electron_domain_geometry,
    molecular_geometry,
    approx_point_group
FROM vsepr_examples
ORDER BY bonding_domains + lone_pair_domains, molecule;

SELECT
    molecule,
    ROUND(AVG(x_angstrom), 6) AS center_geometry_x,
    ROUND(AVG(y_angstrom), 6) AS center_geometry_y,
    ROUND(AVG(z_angstrom), 6) AS center_geometry_z
FROM molecular_coordinates
GROUP BY molecule
ORDER BY molecule;

SELECT
    operation_name,
    operation_type,
    angle_degrees,
    axis
FROM symmetry_operations
ORDER BY operation_name;
