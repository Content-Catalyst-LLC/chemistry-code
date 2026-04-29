#!/usr/bin/env Rscript

# Synthetic polymer chemistry workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/polymer_tradeoff_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

polymers <- read.csv(file.path(data_dir, "polymer_candidates.csv"), stringsAsFactors = FALSE)
fractions <- read.csv(file.path(data_dir, "molar_mass_fractions.csv"), stringsAsFactors = FALSE)
lifecycle <- read.csv(file.path(data_dir, "degradation_lifecycle_notes.csv"), stringsAsFactors = FALSE)

normalize <- function(x) {
  if (max(x) == min(x)) {
    return(rep(0.5, length(x)))
  }
  (x - min(x)) / (max(x) - min(x))
}

calculate_molar_summary <- function(df) {
  Mn <- sum(df$molecule_count * df$molar_mass_g_mol) / sum(df$molecule_count)
  Mw <- sum(df$molecule_count * df$molar_mass_g_mol^2) /
    sum(df$molecule_count * df$molar_mass_g_mol)
  data.frame(
    polymer_id = df$polymer_id[1],
    Mn_g_mol = Mn,
    Mw_g_mol = Mw,
    dispersity = Mw / Mn
  )
}

molar_summary <- do.call(
  rbind,
  lapply(split(fractions, fractions$polymer_id), calculate_molar_summary)
)

polymers$barrier_score <- 1 - normalize(polymers$oxygen_permeability_relative)
polymers$elongation_score <- normalize(polymers$elongation_percent)
polymers$modulus_score <- normalize(polymers$modulus_MPa)
polymers$toughness_proxy <- polymers$elongation_score * polymers$modulus_score
polymers$responsible_design_score <- (
  0.60 * polymers$recyclability_score +
  0.40 * (1 - normalize(polymers$relative_cost_score))
)

polymers$combined_score <- (
  0.45 * polymers$barrier_score +
  0.25 * polymers$toughness_proxy +
  0.30 * polymers$responsible_design_score
)

polymers$rank <- rank(-polymers$combined_score, ties.method = "min")
ranked <- polymers[order(polymers$rank), ]

class_summary <- aggregate(
  combined_score ~ polymer_class,
  data = polymers,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

class_summary_clean <- data.frame(
  polymer_class = class_summary$polymer_class,
  mean_combined_score = class_summary$combined_score[, "mean"],
  max_combined_score = class_summary$combined_score[, "max"],
  candidate_count = class_summary$combined_score[, "n"]
)

write.csv(ranked, file.path(table_dir, "r_polymer_tradeoff_ranking.csv"), row.names = FALSE)
write.csv(class_summary_clean, file.path(table_dir, "r_polymer_class_summary.csv"), row.names = FALSE)
write.csv(molar_summary, file.path(table_dir, "r_polymer_molar_mass_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_polymer_tradeoff_report.txt"))
cat("Synthetic Polymer Chemistry Tradeoff Report\n")
cat("==========================================\n\n")
cat("Molar-mass summary:\n")
print(molar_summary)
cat("\nCandidate ranking:\n")
print(ranked[, c(
  "polymer_id",
  "polymer_class",
  "barrier_score",
  "toughness_proxy",
  "responsible_design_score",
  "combined_score",
  "rank"
)])
cat("\nClass summary:\n")
print(class_summary_clean)
cat("\nLifecycle records:\n")
print(lifecycle)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R polymer tradeoff workflow complete.")
