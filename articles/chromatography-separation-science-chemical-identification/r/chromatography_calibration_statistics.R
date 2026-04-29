#!/usr/bin/env Rscript

# Synthetic chromatography calibration and replicate workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/chromatography_calibration_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

calibration <- read.csv(file.path(data_dir, "calibration_peak_areas.csv"), stringsAsFactors = FALSE)
peaks <- read.csv(file.path(data_dir, "chromatographic_peaks.csv"), stringsAsFactors = FALSE)

standards <- calibration[calibration$standard_id == "blank" | grepl("^std_", calibration$standard_id), ]
unknowns <- calibration[grepl("^unknown", calibration$standard_id), ]

calibration_model <- lm(peak_area ~ concentration_mg_l, data = standards)

intercept <- coef(calibration_model)[1]
slope <- coef(calibration_model)[2]

unknowns$estimated_concentration_mg_l <- (unknowns$peak_area - intercept) / slope

unknown_summary <- data.frame(
  compound = "caffeine",
  mean_peak_area = mean(unknowns$peak_area),
  sd_peak_area = sd(unknowns$peak_area),
  mean_concentration_mg_l = mean(unknowns$estimated_concentration_mg_l),
  sd_concentration_mg_l = sd(unknowns$estimated_concentration_mg_l),
  replicate_count = nrow(unknowns)
)

peak_summary <- aggregate(
  peak_area ~ sample_id,
  data = peaks,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

peak_summary_clean <- data.frame(
  sample_id = peak_summary$sample_id,
  mean_peak_area = peak_summary$peak_area[, "mean"],
  max_peak_area = peak_summary$peak_area[, "max"],
  peak_count = peak_summary$peak_area[, "n"]
)

write.csv(unknowns, file.path(table_dir, "r_chromatography_unknown_estimates.csv"), row.names = FALSE)
write.csv(unknown_summary, file.path(table_dir, "r_chromatography_unknown_summary.csv"), row.names = FALSE)
write.csv(peak_summary_clean, file.path(table_dir, "r_chromatography_peak_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_chromatography_statistics_report.txt"))
cat("Synthetic Chromatography Statistics Report\n")
cat("=========================================\n\n")
cat("Calibration model:\n")
print(summary(calibration_model))
cat("\nUnknown summary:\n")
print(unknown_summary)
cat("\nPeak summary:\n")
print(peak_summary_clean)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R chromatography statistics workflow complete.")
