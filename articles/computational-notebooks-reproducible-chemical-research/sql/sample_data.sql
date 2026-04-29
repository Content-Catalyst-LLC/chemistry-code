-- Minimal sample inserts matching the synthetic CSV.

INSERT INTO notebook_environment (
    environment_id,
    python_version,
    r_version,
    julia_version,
    operating_system,
    dependency_lockfile,
    container_image,
    notes
) VALUES (
    'py311_r443',
    '3.11',
    '4.4.3',
    '1.11',
    'portable educational environment',
    'requirements.txt / renv.lock / Project.toml',
    'not specified',
    'Synthetic educational environment record.'
);

INSERT INTO chemical_notebook_run (
    run_id, notebook_id, molecule, method, instrument_id, environment_id,
    concentration_mol_l, absorbance, temperature_k, analyst, random_seed, execution_order
) VALUES
('run_001', 'uvvis_calibration_v1', 'caffeine', 'UV-Vis', 'uvvis_A', 'py311_r443', 0.000, 0.006, 298.15, 'analyst_alpha', 101, 1),
('run_002', 'uvvis_calibration_v1', 'caffeine', 'UV-Vis', 'uvvis_A', 'py311_r443', 0.002, 0.154, 298.16, 'analyst_alpha', 101, 2),
('run_003', 'uvvis_calibration_v1', 'caffeine', 'UV-Vis', 'uvvis_A', 'py311_r443', 0.004, 0.301, 298.14, 'analyst_alpha', 101, 3),
('run_004', 'uvvis_calibration_v1', 'caffeine', 'UV-Vis', 'uvvis_A', 'py311_r443', 0.006, 0.453, 298.15, 'analyst_alpha', 101, 4),
('run_005', 'uvvis_calibration_v1', 'caffeine', 'UV-Vis', 'uvvis_A', 'py311_r443', 0.008, 0.602, 298.17, 'analyst_alpha', 101, 5),
('run_006', 'uvvis_calibration_v1', 'caffeine', 'UV-Vis', 'uvvis_A', 'py311_r443', 0.010, 0.748, 298.15, 'analyst_alpha', 101, 6);
