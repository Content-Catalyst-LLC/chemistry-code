#!/usr/bin/env Rscript

# Synthetic nanomaterial replicate and stability workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/nanochemistry_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

replicates <- read.csv(file.path(data_dir, "nanoparticle_replicates.csv"), stringsAsFactors = FALSE)
candidates <- read.csv(file.path(data_dir, "nanomaterial_candidates.csv"), stringsAsFactors = FALSE)
stability <- read.csv(file.path(data_dir, "stability_media_tests.csv"), stringsAsFactors = FALSE)

summary_table <- aggregate(
  cbind(core_diameter_nm, hydrodynamic_diameter_nm, polydispersity_index, aggregation_after_salt_relative) ~ sample_id,
  data = replicates,
  FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x))
)

summary_clean <- data.frame(
  sample_id = summary_table$sample_id,
  mean_core_diameter_nm = summary_table$core_diameter_nm[, "mean"],
  sd_core_diameter_nm = summary_table$core_diameter_nm[, "sd"],
  mean_hydrodynamic_diameter_nm = summary_table$hydrodynamic_diameter_nm[, "mean"],
  sd_hydrodynamic_diameter_nm = summary_table$hydrodynamic_diameter_nm[, "sd"],
  mean_polydispersity_index = summary_table$polydispersity_index[, "mean"],
  mean_aggregation_after_salt_relative = summary_table$aggregation_after_salt_relative[, "mean"],
  replicate_count = summary_table$core_diameter_nm[, "n"]
)

summary_clean$stability_review_required <- (
  summary_clean$mean_polydispersity_index > 0.25 |
  summary_clean$mean_aggregation_after_salt_relative > 0.30
)

class_summary <- aggregate(
  core_diameter_nm ~ material_class,
  data = candidates,
  FUN = function(x) c(mean = mean(x), min = min(x), max = max(x), n = length(x))
)

class_summary_clean <- data.frame(
  material_class = class_summary$material_class,
  mean_core_diameter_nm = class_summary$core_diameter_nm[, "mean"],
  min_core_diameter_nm = class_summary$core_diameter_nm[, "min"],
  max_core_diameter_nm = class_summary$core_diameter_nm[, "max"],
  candidate_count = class_summary$core_diameter_nm[, "n"]
)

stability_flags <- stability[stability$aggregation_flag == "true", ]

write.csv(summary_clean, file.path(table_dir, "r_nanoparticle_replicate_summary.csv"), row.names = FALSE)
write.csv(class_summary_clean, file.path(table_dir, "r_nanomaterial_class_summary.csv"), row.names = FALSE)
write.csv(stability_flags, file.path(table_dir, "r_stability_flags.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_nanochemistry_statistics_report.txt"))
cat("Synthetic Nanochemistry Statistics Report\n")
cat("========================================\n\n")
cat("Replicate measurement summary:\n")
print(summary_clean)
cat("\nClass summary:\n")
print(class_summary_clean)
cat("\nStability flags:\n")
print(stability_flags)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R nanochemistry statistics workflow complete.")
