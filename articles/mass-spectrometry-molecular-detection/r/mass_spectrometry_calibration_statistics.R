#!/usr/bin/env Rscript

# Synthetic mass spectrometry calibration and replicate workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/mass_spectrometry_calibration_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

calibration <- read.csv(file.path(data_dir, "ms_calibration.csv"), stringsAsFactors = FALSE)
features <- read.csv(file.path(data_dir, "ms_features.csv"), stringsAsFactors = FALSE)

standards <- calibration[calibration$standard_id == "blank" | grepl("^std_", calibration$standard_id), ]
unknowns <- calibration[grepl("^unknown", calibration$standard_id), ]

calibration_model <- lm(peak_area ~ concentration_ng_ml, data = standards)

intercept <- coef(calibration_model)[1]
slope <- coef(calibration_model)[2]

unknowns$estimated_concentration_ng_ml <- (unknowns$peak_area - intercept) / slope

unknown_summary <- data.frame(
  compound = "caffeine_candidate",
  mean_peak_area = mean(unknowns$peak_area),
  sd_peak_area = sd(unknowns$peak_area),
  mean_concentration_ng_ml = mean(unknowns$estimated_concentration_ng_ml),
  sd_concentration_ng_ml = sd(unknowns$estimated_concentration_ng_ml),
  replicate_count = nrow(unknowns)
)

feature_summary <- aggregate(
  peak_area ~ sample_id + charge,
  data = features,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

feature_summary_clean <- data.frame(
  sample_id = feature_summary$sample_id,
  charge = feature_summary$charge,
  mean_peak_area = feature_summary$peak_area[, "mean"],
  max_peak_area = feature_summary$peak_area[, "max"],
  feature_count = feature_summary$peak_area[, "n"]
)

write.csv(unknowns, file.path(table_dir, "r_ms_unknown_estimates.csv"), row.names = FALSE)
write.csv(unknown_summary, file.path(table_dir, "r_ms_unknown_summary.csv"), row.names = FALSE)
write.csv(feature_summary_clean, file.path(table_dir, "r_ms_feature_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_mass_spectrometry_statistics_report.txt"))
cat("Synthetic Mass Spectrometry Statistics Report\n")
cat("============================================\n\n")
cat("Calibration model:\n")
print(summary(calibration_model))
cat("\nUnknown summary:\n")
print(unknown_summary)
cat("\nFeature summary:\n")
print(feature_summary_clean)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R mass spectrometry statistics workflow complete.")
