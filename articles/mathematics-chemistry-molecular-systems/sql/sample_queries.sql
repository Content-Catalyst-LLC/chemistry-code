.mode column
.headers on

SELECT
    reaction,
    reactant,
    reactant_moles,
    product,
    ROUND(reactant_moles * coefficient_product / coefficient_reactant, 6) AS product_moles
FROM stoichiometry_examples;

SELECT
    solution,
    hydrogen_activity,
    ROUND(-LOG(hydrogen_activity) / LOG(10), 4) AS pH
FROM ph_examples
ORDER BY pH;

SELECT
    reaction,
    delta_g_standard_kj_mol,
    temperature_k,
    ROUND(EXP(-(delta_g_standard_kj_mol * 1000.0) / (8.314462618 * temperature_k)), 6) AS equilibrium_constant
FROM thermodynamics_examples;

SELECT
    molecule,
    atom_i,
    atom_j,
    bond_order
FROM molecular_graph_edges
ORDER BY molecule, atom_i, atom_j;
