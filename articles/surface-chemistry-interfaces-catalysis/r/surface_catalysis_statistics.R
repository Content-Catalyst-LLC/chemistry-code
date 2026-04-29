#!/usr/bin/env Rscript

# Synthetic surface chemistry and catalysis workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/surface_catalysis_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

performance <- read.csv(file.path(data_dir, "catalyst_performance.csv"), stringsAsFactors = FALSE)
deactivation <- read.csv(file.path(data_dir, "deactivation_time_series.csv"), stringsAsFactors = FALSE)
catalysts <- read.csv(file.path(data_dir, "catalyst_candidates.csv"), stringsAsFactors = FALSE)

summary_table <- aggregate(
  cbind(conversion_percent, selectivity_percent) ~ catalyst_id,
  data = performance,
  FUN = function(x) c(mean = mean(x), sd = sd(x), n = length(x))
)

summary_clean <- data.frame(
  catalyst_id = summary_table$catalyst_id,
  mean_conversion_percent = summary_table$conversion_percent[, "mean"],
  sd_conversion_percent = summary_table$conversion_percent[, "sd"],
  replicate_count = summary_table$conversion_percent[, "n"],
  mean_selectivity_percent = summary_table$selectivity_percent[, "mean"],
  sd_selectivity_percent = summary_table$selectivity_percent[, "sd"]
)

deactivation_summaries <- do.call(
  rbind,
  lapply(split(deactivation, deactivation$catalyst_id), function(df) {
    model <- lm(normalized_rate ~ time_h, data = df)
    data.frame(
      catalyst_id = df$catalyst_id[1],
      deactivation_slope_per_h = coef(model)[2],
      initial_rate = df$normalized_rate[1],
      final_rate = df$normalized_rate[nrow(df)],
      percent_rate_loss = 100 * (df$normalized_rate[1] - df$normalized_rate[nrow(df)]) / df$normalized_rate[1]
    )
  })
)

class_summary <- aggregate(
  surface_area_m2_g ~ catalyst_class,
  data = catalysts,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

class_summary_clean <- data.frame(
  catalyst_class = class_summary$catalyst_class,
  mean_surface_area_m2_g = class_summary$surface_area_m2_g[, "mean"],
  max_surface_area_m2_g = class_summary$surface_area_m2_g[, "max"],
  catalyst_count = class_summary$surface_area_m2_g[, "n"]
)

write.csv(summary_clean, file.path(table_dir, "r_catalyst_replicate_summary.csv"), row.names = FALSE)
write.csv(deactivation_summaries, file.path(table_dir, "r_catalyst_deactivation_summary.csv"), row.names = FALSE)
write.csv(class_summary_clean, file.path(table_dir, "r_catalyst_class_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_surface_catalysis_statistics_report.txt"))
cat("Synthetic Surface Catalysis Statistics Report\n")
cat("============================================\n\n")
cat("Catalyst replicate summary:\n")
print(summary_clean)
cat("\nDeactivation summaries:\n")
print(deactivation_summaries)
cat("\nCatalyst class summary:\n")
print(class_summary_clean)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R surface catalysis statistics workflow complete.")
