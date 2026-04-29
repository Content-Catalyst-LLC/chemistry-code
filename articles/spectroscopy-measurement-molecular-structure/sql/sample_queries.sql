-- Sample queries for synthetic spectroscopy workflows.

-- 1. IR peaks in the carbonyl-region teaching window.
SELECT
    peak_id,
    wavenumber_cm_minus_1,
    relative_intensity,
    educational_assignment
FROM ir_peak
WHERE wavenumber_cm_minus_1 BETWEEN 1650 AND 1800
ORDER BY relative_intensity DESC;

-- 2. Spectroscopic methods used for each sample.
SELECT
    sample_id,
    method,
    instrument_id,
    temperature_k
FROM spectral_measurement
ORDER BY sample_id, method;

-- 3. UV-visible calibration records by wavelength.
SELECT
    wavelength_nm,
    concentration_mol_l,
    absorbance,
    path_length_cm
FROM uvvis_measurement
ORDER BY wavelength_nm, concentration_mol_l;

-- 4. NMR signals ordered by chemical shift.
SELECT
    chemical_shift_ppm,
    integration,
    multiplicity,
    educational_region
FROM nmr_signal
ORDER BY chemical_shift_ppm DESC;
