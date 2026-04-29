#!/usr/bin/env Rscript

# Synthetic colloid and complex-fluid replicate workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/colloid_rheology_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

replicates <- read.csv(file.path(data_dir, "rheology_replicates.csv"), stringsAsFactors = FALSE)
systems <- read.csv(file.path(data_dir, "colloid_systems.csv"), stringsAsFactors = FALSE)
stability <- read.csv(file.path(data_dir, "stability_tests.csv"), stringsAsFactors = FALSE)

summary_table <- aggregate(
  cbind(low_shear_viscosity_Pa_s, high_shear_viscosity_Pa_s, yield_stress_Pa, salt_aggregation_index) ~ formulation_id,
  data = replicates,
  FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x))
)

summary_clean <- data.frame(
  formulation_id = summary_table$formulation_id,
  mean_low_shear_viscosity_Pa_s = summary_table$low_shear_viscosity_Pa_s[, "mean"],
  sd_low_shear_viscosity_Pa_s = summary_table$low_shear_viscosity_Pa_s[, "sd"],
  mean_high_shear_viscosity_Pa_s = summary_table$high_shear_viscosity_Pa_s[, "mean"],
  sd_high_shear_viscosity_Pa_s = summary_table$high_shear_viscosity_Pa_s[, "sd"],
  mean_yield_stress_Pa = summary_table$yield_stress_Pa[, "mean"],
  mean_salt_aggregation_index = summary_table$salt_aggregation_index[, "mean"],
  replicate_count = summary_table$yield_stress_Pa[, "n"]
)

summary_clean$shear_thinning_ratio <- (
  summary_clean$mean_low_shear_viscosity_Pa_s /
  summary_clean$mean_high_shear_viscosity_Pa_s
)

summary_clean$review_required <- (
  summary_clean$mean_yield_stress_Pa > 10 |
  summary_clean$mean_salt_aggregation_index > 0.30 |
  summary_clean$shear_thinning_ratio > 10
)

type_summary <- aggregate(
  volume_fraction ~ system_type,
  data = systems,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

type_summary_clean <- data.frame(
  system_type = type_summary$system_type,
  mean_volume_fraction = type_summary$volume_fraction[, "mean"],
  max_volume_fraction = type_summary$volume_fraction[, "max"],
  system_count = type_summary$volume_fraction[, "n"]
)

stability_flags <- stability[
  stability$aggregation_flag == "true" |
  stability$phase_separation_index > 0.20 |
  stability$sedimentation_index > 0.20 |
  stability$creaming_index > 0.20,
]

write.csv(summary_clean, file.path(table_dir, "r_colloid_rheology_replicate_summary.csv"), row.names = FALSE)
write.csv(type_summary_clean, file.path(table_dir, "r_colloid_type_summary.csv"), row.names = FALSE)
write.csv(stability_flags, file.path(table_dir, "r_stability_flags.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_colloid_rheology_report.txt"))
cat("Synthetic Colloid and Soft Matter Report\n")
cat("=======================================\n\n")
cat("Replicate rheology and stability summary:\n")
print(summary_clean)
cat("\nSystem type summary:\n")
print(type_summary_clean)
cat("\nStability flags:\n")
print(stability_flags)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R colloid rheology workflow complete.")
