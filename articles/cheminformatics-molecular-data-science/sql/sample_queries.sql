.headers on
.mode column

SELECT
    m.molecule_id,
    m.name,
    d.heavy_atoms,
    d.hetero_atoms,
    ROUND(CAST(d.hetero_atoms AS REAL) / d.heavy_atoms, 3) AS hetero_atom_fraction,
    d.h_bond_donors + d.h_bond_acceptors AS polarity_score
FROM molecules m
JOIN descriptors d ON m.molecule_id = d.molecule_id
ORDER BY m.molecule_id;

SELECT
    molecule_id,
    ROUND(
      (bit_1 + bit_2 + bit_3 + bit_4 + bit_5 + bit_6 + bit_7 + bit_8 + bit_9 + bit_10),
      3
    ) AS active_fingerprint_bits
FROM fingerprints
ORDER BY molecule_id;

SELECT
    compound_id,
    target_id,
    value AS ic50_nM,
    ROUND(-LOG10(value * 1e-9), 6) AS pIC50
FROM assays
WHERE LOWER(unit) = 'nm'
ORDER BY pIC50 DESC;

SELECT
    split,
    scaffold,
    COUNT(*) AS molecule_count
FROM scaffold_splits
GROUP BY split, scaffold
ORDER BY split, scaffold;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
