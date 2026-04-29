-- Sample queries for synthetic colloid and complex-fluid workflows.

-- 1. Systems requiring stability or rheology review.
SELECT
    formulation_id,
    system_type,
    zeta_potential_mV,
    volume_fraction,
    yield_stress_Pa,
    salt_aggregation_index
FROM colloid_system
WHERE ABS(zeta_potential_mV) < 20
   OR volume_fraction > 0.25
   OR yield_stress_Pa > 10
   OR salt_aggregation_index > 0.30
ORDER BY salt_aggregation_index DESC;

-- 2. Rheology replicate summary.
SELECT
    formulation_id,
    COUNT(*) AS replicate_count,
    AVG(low_shear_viscosity_Pa_s) AS mean_low_shear_viscosity_Pa_s,
    AVG(high_shear_viscosity_Pa_s) AS mean_high_shear_viscosity_Pa_s,
    AVG(yield_stress_Pa) AS mean_yield_stress_Pa
FROM rheology_replicate
GROUP BY formulation_id
ORDER BY mean_yield_stress_Pa DESC;

-- 3. Stability tests with failure flags.
SELECT
    formulation_id,
    condition,
    temperature_C,
    storage_days,
    phase_separation_index,
    sedimentation_index,
    creaming_index,
    aggregation_flag
FROM stability_test
WHERE aggregation_flag = 1
   OR phase_separation_index > 0.20
   OR sedimentation_index > 0.20
   OR creaming_index > 0.20
ORDER BY formulation_id, condition;

-- 4. Emulsion droplet and coalescence records.
SELECT
    emulsion_id,
    formulation_id,
    oil_phase,
    surfactant_class,
    mean_droplet_size_nm,
    polydispersity_index,
    coalescence_index
FROM emulsion_property
ORDER BY coalescence_index DESC;

-- 5. Responsible formulation review.
SELECT
    c.formulation_id,
    c.system_type,
    l.additive_review_required,
    l.particle_exposure_review,
    l.wastewater_fate_note,
    l.responsible_formulation_review
FROM lifecycle_note l
JOIN colloid_system c
    ON l.formulation_id = c.formulation_id
WHERE l.responsible_formulation_review = 1
ORDER BY c.formulation_id;
