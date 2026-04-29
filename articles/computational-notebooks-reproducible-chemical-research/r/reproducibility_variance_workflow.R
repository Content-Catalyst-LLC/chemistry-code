#!/usr/bin/env Rscript

# Statistical reproducibility summary for synthetic chemical notebook data.
# This script uses base R so it can run in a minimal R environment.
# The data are synthetic and educational only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/reproducibility_variance_workflow.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_path <- file.path(base_dir, "data", "synthetic_chemical_notebook_runs.csv")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

runs <- read.csv(data_path, stringsAsFactors = FALSE)

calibration_model <- lm(absorbance ~ concentration_mol_l, data = runs)

summary_by_notebook <- aggregate(
  absorbance ~ notebook_id + instrument_id + environment_id,
  data = runs,
  FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x))
)

summary_clean <- data.frame(
  notebook_id = summary_by_notebook$notebook_id,
  instrument_id = summary_by_notebook$instrument_id,
  environment_id = summary_by_notebook$environment_id,
  mean_absorbance = summary_by_notebook$absorbance[, "mean"],
  sd_absorbance = summary_by_notebook$absorbance[, "sd"],
  n = summary_by_notebook$absorbance[, "n"]
)

write.csv(
  summary_clean,
  file = file.path(table_dir, "r_notebook_instrument_summary.csv"),
  row.names = FALSE
)

sink(file.path(report_dir, "r_reproducibility_report.txt"))
cat("R Reproducibility Summary for Synthetic Chemical Notebook Data\n")
cat("=============================================================\n\n")
cat("Calibration model: absorbance ~ concentration_mol_l\n\n")
print(summary(calibration_model))
cat("\nNotebook and instrument summary:\n")
print(summary_clean)
cat("\nResponsible-use note:\n")
cat("Synthetic educational data only. Do not use for regulatory, clinical, safety-critical, or environmental-compliance decisions.\n")
sink()

message("R reproducibility workflow complete.")
