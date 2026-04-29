-- Sample queries for synthetic electrochemistry, batteries, and energy-storage workflows.

-- 1. Candidate cells with high critical-material or safety review scores.
SELECT
    cell_id,
    chemistry,
    nominal_voltage_V,
    specific_capacity_mAh_g,
    cycle_100_capacity_retention,
    critical_material_score,
    safety_review_score
FROM cell_candidate
WHERE critical_material_score > 0.60
   OR safety_review_score > 0.40
ORDER BY critical_material_score DESC, safety_review_score DESC;

-- 2. Capacity retention and coulombic efficiency by cycle.
SELECT
    cell_id,
    cycle_number,
    discharge_capacity_mAh,
    charge_capacity_mAh,
    discharge_capacity_mAh / charge_capacity_mAh AS coulombic_efficiency
FROM cycling_data
ORDER BY cell_id, cycle_number;

-- 3. Final-cycle cells below 90 percent capacity retention.
WITH initial AS (
    SELECT cell_id, discharge_capacity_mAh AS initial_capacity
    FROM cycling_data
    WHERE cycle_number = 1
),
final AS (
    SELECT cell_id, discharge_capacity_mAh AS final_capacity
    FROM cycling_data
    WHERE cycle_number = 100
)
SELECT
    f.cell_id,
    c.chemistry,
    f.final_capacity / i.initial_capacity AS final_capacity_retention
FROM final f
JOIN initial i ON f.cell_id = i.cell_id
JOIN cell_candidate c ON f.cell_id = c.cell_id
WHERE f.final_capacity / i.initial_capacity < 0.90
ORDER BY final_capacity_retention ASC;

-- 4. Impedance review at final cycle.
SELECT
    cell_id,
    cycle_number,
    ohmic_resistance_mOhm,
    charge_transfer_resistance_mOhm,
    diffusion_tail_score
FROM impedance_measurement
WHERE cycle_number = 100
  AND (charge_transfer_resistance_mOhm > 150 OR diffusion_tail_score > 0.75)
ORDER BY charge_transfer_resistance_mOhm DESC;

-- 5. Responsible lifecycle review.
SELECT
    c.cell_id,
    c.chemistry,
    l.critical_material_review,
    l.safety_review_required,
    l.recycling_pathway,
    l.end_of_life_note
FROM lifecycle_note l
JOIN cell_candidate c
    ON l.cell_id = c.cell_id
WHERE l.responsible_design_review = 1
ORDER BY c.cell_id;
