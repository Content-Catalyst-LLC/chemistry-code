#!/usr/bin/env Rscript

# Synthetic electrochemical sensor calibration, drift, and replicate workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/electrochemical_sensor_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

calibration <- read.csv(file.path(data_dir, "sensor_calibration.csv"), stringsAsFactors = FALSE)
unknowns <- read.csv(file.path(data_dir, "unknown_sensor_samples.csv"), stringsAsFactors = FALSE)
drift <- read.csv(file.path(data_dir, "sensor_drift.csv"), stringsAsFactors = FALSE)
interferences <- read.csv(file.path(data_dir, "interference_tests.csv"), stringsAsFactors = FALSE)

calibration_model <- lm(current_uA ~ concentration_uM, data = calibration)

intercept <- coef(calibration_model)[1]
slope <- coef(calibration_model)[2]

unknowns$estimated_concentration_uM <- (unknowns$current_uA - intercept) / slope

unknown_summary <- aggregate(
  estimated_concentration_uM ~ sample_id,
  data = unknowns,
  FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x))
)

unknown_summary_clean <- data.frame(
  sample_id = unknown_summary$sample_id,
  mean_concentration_uM = unknown_summary$estimated_concentration_uM[, "mean"],
  sd_concentration_uM = unknown_summary$estimated_concentration_uM[, "sd"],
  replicate_count = unknown_summary$estimated_concentration_uM[, "n"]
)

drift_model <- lm(current_uA ~ time_min, data = drift)

drift_summary <- data.frame(
  drift_slope_uA_per_min = coef(drift_model)[2],
  initial_current_uA = drift$current_uA[1],
  final_current_uA = drift$current_uA[nrow(drift)],
  percent_change = 100 * (drift$current_uA[nrow(drift)] - drift$current_uA[1]) / drift$current_uA[1]
)

interference_flags <- interferences[abs(interferences$response_change_percent) >= 5, ]

write.csv(unknowns, file.path(table_dir, "r_electrochemical_unknown_estimates.csv"), row.names = FALSE)
write.csv(unknown_summary_clean, file.path(table_dir, "r_electrochemical_unknown_summary.csv"), row.names = FALSE)
write.csv(drift_summary, file.path(table_dir, "r_electrochemical_drift_summary.csv"), row.names = FALSE)
write.csv(interference_flags, file.path(table_dir, "r_interference_flags.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_electrochemical_sensor_statistics_report.txt"))
cat("Synthetic Electrochemical Sensor Statistics Report\n")
cat("=================================================\n\n")
cat("Calibration model:\n")
print(summary(calibration_model))
cat("\nUnknown summary:\n")
print(unknown_summary_clean)
cat("\nDrift summary:\n")
print(drift_summary)
cat("\nInterference flags:\n")
print(interference_flags)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R electrochemical sensor statistics workflow complete.")
