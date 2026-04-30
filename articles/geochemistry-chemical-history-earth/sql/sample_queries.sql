-- Sample query 1: simplified Chemical Index of Alteration.
-- Teaching-only version using weight percentages and uncorrected CaO.
SELECT
    s.sample_id,
    s.rock_type,
    100.0 * m.Al2O3_wt_pct /
        (m.Al2O3_wt_pct + m.CaO_wt_pct + m.Na2O_wt_pct + m.K2O_wt_pct)
        AS CIA_simplified
FROM major_oxides m
JOIN geochemical_samples s ON m.sample_id = s.sample_id;

-- Sample query 2: Rb/Sr ratio from trace element rows.
SELECT
    rb.sample_id,
    rb.concentration_ppm AS Rb_ppm,
    sr.concentration_ppm AS Sr_ppm,
    rb.concentration_ppm / sr.concentration_ppm AS Rb_Sr_ratio
FROM trace_elements rb
JOIN trace_elements sr ON rb.sample_id = sr.sample_id
WHERE rb.element_symbol = 'Rb'
  AND sr.element_symbol = 'Sr'
  AND sr.concentration_ppm > 0;

-- Sample query 3: simplified parent-daughter age.
SELECT
    sample_id,
    parent_isotope_units,
    radiogenic_daughter_units,
    decay_constant_per_year,
    (1.0 / decay_constant_per_year) *
      ln(1.0 + radiogenic_daughter_units / parent_isotope_units) / 1000000.0
      AS age_Ma_simplified
FROM radiometric_systems
WHERE parent_isotope_units > 0;
