#!/usr/bin/env Rscript

# Synthetic materials chemistry tradeoff workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/materials_tradeoff_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

materials <- read.csv(file.path(data_dir, "material_candidates.csv"), stringsAsFactors = FALSE)
lifecycle <- read.csv(file.path(data_dir, "lifecycle_notes.csv"), stringsAsFactors = FALSE)
processing <- read.csv(file.path(data_dir, "processing_conditions.csv"), stringsAsFactors = FALSE)

normalize <- function(x) {
  if (max(x) == min(x)) {
    return(rep(0.5, length(x)))
  }
  (x - min(x)) / (max(x) - min(x))
}

materials$modulus_norm <- normalize(materials$modulus_GPa)
materials$thermal_norm <- normalize(materials$thermal_stability_C)
materials$low_density_norm <- 1 - normalize(materials$density_g_cm3)
materials$low_cost_norm <- 1 - normalize(materials$relative_cost_score)

materials$performance_score <- (
  0.35 * materials$modulus_norm +
  0.35 * materials$thermal_norm +
  0.30 * materials$low_density_norm
)

materials$responsible_design_score <- (
  0.55 * materials$recyclability_score +
  0.45 * materials$low_cost_norm
)

materials$combined_score <- (
  0.60 * materials$performance_score +
  0.40 * materials$responsible_design_score
)

materials$rank <- rank(-materials$combined_score, ties.method = "min")

ranked <- materials[order(materials$rank), ]

class_summary <- aggregate(
  combined_score ~ material_class,
  data = materials,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

class_summary_clean <- data.frame(
  material_class = class_summary$material_class,
  mean_combined_score = class_summary$combined_score[, "mean"],
  max_combined_score = class_summary$combined_score[, "max"],
  candidate_count = class_summary$combined_score[, "n"]
)

write.csv(ranked, file.path(table_dir, "r_materials_tradeoff_ranking.csv"), row.names = FALSE)
write.csv(class_summary_clean, file.path(table_dir, "r_materials_class_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_materials_tradeoff_report.txt"))
cat("Synthetic Materials Chemistry Tradeoff Report\n")
cat("============================================\n\n")
cat("Candidate ranking:\n")
print(ranked[, c(
  "material_id",
  "material_class",
  "performance_score",
  "responsible_design_score",
  "combined_score",
  "rank"
)])
cat("\nClass summary:\n")
print(class_summary_clean)
cat("\nLifecycle records:\n")
print(lifecycle)
cat("\nProcessing records:\n")
print(processing)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R materials tradeoff workflow complete.")
