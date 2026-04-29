#!/usr/bin/env Rscript

# Synthetic spectroscopy statistics workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/spectroscopy_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

uvvis <- read.csv(file.path(data_dir, "uvvis_calibration.csv"), stringsAsFactors = FALSE)
ir <- read.csv(file.path(data_dir, "ir_peaks.csv"), stringsAsFactors = FALSE)
nmr <- read.csv(file.path(data_dir, "nmr_signals.csv"), stringsAsFactors = FALSE)

standards <- uvvis[uvvis$standard_id == "blank" | grepl("^std", uvvis$standard_id), ]
unknowns <- uvvis[grepl("^unknown", uvvis$standard_id), ]

calibration_model <- lm(absorbance ~ concentration_mol_l, data = standards)

intercept <- coef(calibration_model)[1]
slope <- coef(calibration_model)[2]

unknowns$estimated_concentration_mol_l <- (unknowns$absorbance - intercept) / slope

unknown_summary <- data.frame(
  sample_group = "unknown_A",
  mean_absorbance = mean(unknowns$absorbance),
  sd_absorbance = sd(unknowns$absorbance),
  mean_concentration_mol_l = mean(unknowns$estimated_concentration_mol_l),
  sd_concentration_mol_l = sd(unknowns$estimated_concentration_mol_l)
)

ir_summary <- aggregate(
  relative_intensity ~ sample_id,
  data = ir,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

ir_summary_clean <- data.frame(
  sample_id = ir_summary$sample_id,
  mean_relative_intensity = ir_summary$relative_intensity[, "mean"],
  max_relative_intensity = ir_summary$relative_intensity[, "max"],
  peak_count = ir_summary$relative_intensity[, "n"]
)

write.csv(unknowns, file.path(table_dir, "r_uvvis_unknown_estimates.csv"), row.names = FALSE)
write.csv(unknown_summary, file.path(table_dir, "r_uvvis_unknown_summary.csv"), row.names = FALSE)
write.csv(ir_summary_clean, file.path(table_dir, "r_ir_peak_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_spectroscopy_statistics_report.txt"))
cat("Synthetic Spectroscopy Statistics Report\n")
cat("=======================================\n\n")
cat("UV-visible calibration model:\n")
print(summary(calibration_model))
cat("\nUnknown summary:\n")
print(unknown_summary)
cat("\nIR peak summary:\n")
print(ir_summary_clean)
cat("\nNMR synthetic signals:\n")
print(nmr)
cat("\nResponsible-use note: educational synthetic data only.\n")
sink()

message("R spectroscopy statistics workflow complete.")
