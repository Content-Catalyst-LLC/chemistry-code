.headers on
.mode column

SELECT
    case_id,
    acid,
    Ka,
    initial_concentration_mol_l
FROM weak_acid_cases
ORDER BY case_id;

SELECT
    case_id,
    buffer,
    pKa,
    weak_acid_mol_l,
    conjugate_base_mol_l
FROM buffer_cases
ORDER BY case_id;

SELECT
    case_id,
    system,
    pKa1,
    pKa2,
    pKa3
FROM polyprotic_cases
ORDER BY case_id;

SELECT
    operation,
    script,
    output_artifact,
    notes
FROM workflow_steps
ORDER BY step_id;
