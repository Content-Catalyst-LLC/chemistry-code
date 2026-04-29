-- Sample queries for synthetic nanochemistry workflows.

-- 1. Nanoscale candidates with colloidal review flags.
SELECT
    sample_id,
    material_class,
    core_diameter_nm,
    hydrodynamic_diameter_nm,
    zeta_potential_mV,
    polydispersity_index,
    aggregation_after_salt_relative
FROM nanomaterial_candidate
WHERE polydispersity_index > 0.25
   OR aggregation_after_salt_relative > 0.30
   OR ABS(zeta_potential_mV) < 15.0
ORDER BY aggregation_after_salt_relative DESC;

-- 2. Ligand shells by material.
SELECT
    n.sample_id,
    n.material_class,
    l.ligand_class,
    l.functional_group,
    l.coverage_relative,
    l.stabilization_mode
FROM nanomaterial_candidate n
JOIN ligand_shell l
    ON n.sample_id = l.sample_id
ORDER BY n.sample_id;

-- 3. Stability tests with aggregation flags.
SELECT
    sample_id,
    medium,
    pH,
    ionic_strength_mM,
    hydrodynamic_diameter_after_h_nm,
    aggregation_flag
FROM stability_media_test
WHERE aggregation_flag = 1
ORDER BY sample_id, medium;

-- 4. Lifecycle and exposure review.
SELECT
    n.sample_id,
    n.material_class,
    l.critical_material_flag,
    l.dissolution_or_transformation_concern,
    l.exposure_review_required,
    l.end_of_life_note
FROM lifecycle_note l
JOIN nanomaterial_candidate n
    ON l.sample_id = n.sample_id
WHERE l.exposure_review_required IN ('medium', 'high')
   OR l.critical_material_flag = 1
ORDER BY l.exposure_review_required DESC;

-- 5. Optical nanoscale materials.
SELECT
    sample_id,
    material_class,
    core_diameter_nm,
    absorbance_peak_nm,
    emission_peak_nm,
    quantum_yield_relative,
    photostability_relative
FROM optical_property
ORDER BY core_diameter_nm;
