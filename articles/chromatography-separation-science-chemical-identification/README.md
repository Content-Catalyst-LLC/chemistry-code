# Chromatography, Separation Science, and Chemical Identification

This article folder supports the Chemistry knowledge-series article **Chromatography, Separation Science, and Chemical Identification**.

The workflows use synthetic educational data to demonstrate retention factors, adjacent-peak resolution, calibration, tentative candidate matching, chromatographic provenance, and full-stack scientific-computing scaffolding.

## Repository structure

- `python/` — retention, resolution, candidate matching, calibration, and provenance workflows
- `r/` — calibration regression, replicate summaries, and quantitative reporting
- `julia/` — retention-factor and resolution calculations
- `fortran/` — compact chromatography metric kernel
- `rust/` — chromatographic manifest validator
- `go/` — CSV audit utility for peak records
- `c/` — retention-factor and resolution utility
- `cpp/` — retention-time candidate classifier
- `sql/` — schema and queries for chromatographic measurements, peaks, and identifications
- `docs/` — methodology, reproducibility, and responsible-use notes
- `data/` — synthetic educational chromatographic data
- `notebooks/` — notebook scaffolds and report notes
- `outputs/` — generated tables, reports, figures, and manifests

## Responsible-use note

All data in this folder are synthetic and educational. Retention-time matching alone is not definitive chemical identification. These workflows are not validated for clinical, forensic, pharmaceutical, environmental-compliance, industrial-quality, or safety-critical use.

## License

This article folder follows the MIT-licensed repository convention used for the Chemistry code collection.
