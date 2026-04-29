# Mass Spectrometry and Molecular Detection

This article folder supports the Chemistry knowledge-series article **Mass Spectrometry and Molecular Detection**.

The workflows use synthetic educational data to demonstrate exact-mass matching, mass-error calculations, isotope-spacing charge estimation, MS/MS fragment evidence, calibration, molecular-detection reporting, and full-stack scientific-computing scaffolding.

## Repository structure

- `python/` — mass accuracy, isotope spacing, candidate matching, calibration, and provenance workflows
- `r/` — calibration regression, replicate summaries, and quantitative reporting
- `julia/` — ppm error and charge-state calculations
- `fortran/` — compact mass-error and resolution kernel
- `rust/` — mass-spectrometry manifest validator
- `go/` — CSV audit utility for MS feature records
- `c/` — mass-error and isotope-spacing utility
- `cpp/` — exact-mass candidate classifier
- `sql/` — schema and queries for MS features, candidates, fragments, and quantitation
- `docs/` — methodology, reproducibility, and responsible-use notes
- `data/` — synthetic educational mass-spectrometry data
- `notebooks/` — notebook scaffolds and report notes
- `outputs/` — generated tables, reports, figures, and manifests

## Responsible-use note

All data in this folder are synthetic and educational. Exact mass alone is not definitive molecular identification. These workflows are not validated for clinical, forensic, pharmaceutical, environmental-compliance, industrial-quality, or safety-critical use.

## License

This article folder follows the MIT-licensed repository convention used for the Chemistry code collection.
