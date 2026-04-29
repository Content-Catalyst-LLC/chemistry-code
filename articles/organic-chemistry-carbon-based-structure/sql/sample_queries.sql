.headers on
.mode column

SELECT
    molecule,
    C,
    H,
    N,
    O,
    S,
    X,
    ROUND(C - (H + X) / 2.0 + N / 2.0 + 1.0, 3) AS DBE
FROM molecular_formulas
ORDER BY molecule;

SELECT
    case_id,
    hybridization,
    approximate_geometry,
    approximate_bond_angle_degrees,
    sigma_bonds,
    pi_bonds
FROM carbon_hybridization_cases
ORDER BY case_id;

SELECT
    molecule,
    alcohol + ether + amine + alkyl_halide + alkene + alkyne + arene + aldehyde + ketone + carboxylic_acid + ester + amide + nitrile + thiol + sulfide AS functional_group_count
FROM functional_group_cases
ORDER BY molecule;

SELECT
    molecule,
    carbon_count,
    heteroatom_count,
    hydrogen_bond_donors,
    hydrogen_bond_acceptors,
    carbon_count + 2 * heteroatom_count + 2 * ring_count + 2 * aromatic_ring_count + 3 * stereocenter_count AS complexity_score
FROM structure_property_cases
ORDER BY complexity_score DESC;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
