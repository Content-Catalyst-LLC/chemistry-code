# Notebook Implementation Notes

This folder is reserved for notebook files connected to the article.

Recommended notebook variants:

1. `uvvis_calibration_audit.ipynb`
   - imports synthetic data;
   - fits the calibration model;
   - writes provenance outputs;
   - validates repeatability from a clean execution.

2. `chemical_notebook_report.qmd`
   - renders a reproducible HTML or PDF report;
   - includes Python and R execution blocks;
   - cites generated outputs from `outputs/tables` and `outputs/manifests`.

Because notebook JSON can be noisy in version control, the repository also includes script equivalents in `python/`, `r/`, and other language folders.
