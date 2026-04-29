-- Reproducibility and provenance queries for synthetic chemical notebooks.

-- 1. Notebook-level run counts and execution-order range.
SELECT
    notebook_id,
    COUNT(*) AS run_count,
    MIN(execution_order) AS first_execution_step,
    MAX(execution_order) AS last_execution_step
FROM chemical_notebook_run
GROUP BY notebook_id
ORDER BY notebook_id;

-- 2. Instrument and environment provenance for each notebook.
SELECT
    notebook_id,
    instrument_id,
    environment_id,
    analyst,
    COUNT(*) AS measurements
FROM chemical_notebook_run
GROUP BY notebook_id, instrument_id, environment_id, analyst
ORDER BY notebook_id;

-- 3. Calibration data ordered by concentration.
SELECT
    concentration_mol_l,
    absorbance,
    temperature_k,
    instrument_id,
    notebook_id
FROM chemical_notebook_run
ORDER BY concentration_mol_l, notebook_id;

-- 4. Temperature range as a simple environmental-stability diagnostic.
SELECT
    notebook_id,
    MIN(temperature_k) AS min_temperature_k,
    MAX(temperature_k) AS max_temperature_k,
    AVG(temperature_k) AS mean_temperature_k
FROM chemical_notebook_run
GROUP BY notebook_id;
