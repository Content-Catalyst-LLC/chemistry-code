#!/usr/bin/env Rscript

# Synthetic electronic and photochemical materials replicate workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/electronic_photochemical_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

device_runs <- read.csv(file.path(data_dir, "device_runs.csv"), stringsAsFactors = FALSE)
stability <- read.csv(file.path(data_dir, "photostability_time_series.csv"), stringsAsFactors = FALSE)
materials <- read.csv(file.path(data_dir, "material_candidates.csv"), stringsAsFactors = FALSE)

summary_table <- aggregate(
  cbind(photocurrent_mA_cm2, open_circuit_voltage_V, fill_factor, photostability_score) ~ material_id,
  data = device_runs,
  FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x))
)

summary_clean <- data.frame(
  material_id = summary_table$material_id,
  mean_photocurrent_mA_cm2 = summary_table$photocurrent_mA_cm2[, "mean"],
  sd_photocurrent_mA_cm2 = summary_table$photocurrent_mA_cm2[, "sd"],
  mean_open_circuit_voltage_V = summary_table$open_circuit_voltage_V[, "mean"],
  mean_fill_factor = summary_table$fill_factor[, "mean"],
  mean_photostability_score = summary_table$photostability_score[, "mean"],
  replicate_count = summary_table$photocurrent_mA_cm2[, "n"]
)

summary_clean$performance_proxy <- (
  summary_clean$mean_photocurrent_mA_cm2 *
  summary_clean$mean_open_circuit_voltage_V *
  summary_clean$mean_fill_factor
)

summary_clean$stability_review_required <- summary_clean$mean_photostability_score < 0.60

stability_summaries <- do.call(
  rbind,
  lapply(split(stability, stability$material_id), function(df) {
    model <- lm(normalized_performance ~ illumination_hours, data = df)
    data.frame(
      material_id = df$material_id[1],
      degradation_slope_per_hour = coef(model)[2],
      initial_performance = df$normalized_performance[1],
      final_performance = df$normalized_performance[nrow(df)],
      percent_performance_loss = 100 * (df$normalized_performance[1] - df$normalized_performance[nrow(df)]) / df$normalized_performance[1]
    )
  })
)

class_summary <- aggregate(
  band_gap_eV ~ material_class,
  data = materials,
  FUN = function(x) c(mean = mean(x), min = min(x), max = max(x), n = length(x))
)

class_summary_clean <- data.frame(
  material_class = class_summary$material_class,
  mean_band_gap_eV = class_summary$band_gap_eV[, "mean"],
  min_band_gap_eV = class_summary$band_gap_eV[, "min"],
  max_band_gap_eV = class_summary$band_gap_eV[, "max"],
  candidate_count = class_summary$band_gap_eV[, "n"]
)

write.csv(summary_clean, file.path(table_dir, "r_device_replicate_summary.csv"), row.names = FALSE)
write.csv(stability_summaries, file.path(table_dir, "r_photostability_summary.csv"), row.names = FALSE)
write.csv(class_summary_clean, file.path(table_dir, "r_material_class_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_electronic_photochemical_report.txt"))
cat("Synthetic Electronic and Photochemical Materials Report\n")
cat("=====================================================\n\n")
cat("Device-like replicate summary:\n")
print(summary_clean)
cat("\nPhotostability summaries:\n")
print(stability_summaries)
cat("\nMaterial class summary:\n")
print(class_summary_clean)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R electronic and photochemical materials workflow complete.")
