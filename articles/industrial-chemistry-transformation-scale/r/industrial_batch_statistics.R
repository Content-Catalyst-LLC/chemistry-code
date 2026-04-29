#!/usr/bin/env Rscript

# Synthetic industrial chemistry batch-analysis workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/industrial_batch_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

batches <- read.csv(file.path(data_dir, "batch_data.csv"), stringsAsFactors = FALSE)
routes <- read.csv(file.path(data_dir, "process_routes.csv"), stringsAsFactors = FALSE)
hazards <- read.csv(file.path(data_dir, "hazard_register.csv"), stringsAsFactors = FALSE)

summary_table <- aggregate(
  cbind(yield_fraction, impurity_percent, energy_kWh_kg, solvent_intensity, temperature_deviation_C) ~ route_id,
  data = batches,
  FUN = function(x) c(mean = mean(x), sd = sd(x), min = min(x), max = max(x))
)

summary_clean <- data.frame(
  route_id = summary_table$route_id,
  mean_yield_fraction = summary_table$yield_fraction[, "mean"],
  sd_yield_fraction = summary_table$yield_fraction[, "sd"],
  min_yield_fraction = summary_table$yield_fraction[, "min"],
  max_yield_fraction = summary_table$yield_fraction[, "max"],
  mean_impurity_percent = summary_table$impurity_percent[, "mean"],
  max_impurity_percent = summary_table$impurity_percent[, "max"],
  mean_energy_kWh_kg = summary_table$energy_kWh_kg[, "mean"],
  mean_solvent_intensity = summary_table$solvent_intensity[, "mean"],
  max_temperature_deviation_C = summary_table$temperature_deviation_C[, "max"]
)

upper_spec_impurity <- 1.00

capability <- aggregate(
  impurity_percent ~ route_id,
  data = batches,
  FUN = function(x) (upper_spec_impurity - mean(x)) / (3 * sd(x))
)

names(capability)[2] <- "simple_cpu_impurity"

summary_clean <- merge(summary_clean, capability, by = "route_id")

summary_clean$quality_review_required <- (
  summary_clean$max_impurity_percent > 0.80 |
  summary_clean$simple_cpu_impurity < 1.33 |
  summary_clean$max_temperature_deviation_C > 2.8
)

routes$yield_fraction <- routes$actual_product_kg / routes$theoretical_product_kg
routes$e_factor <- routes$waste_kg / routes$actual_product_kg
routes$solvent_intensity <- routes$solvent_kg / routes$actual_product_kg
routes$energy_intensity_kWh_kg <- routes$energy_kWh / routes$actual_product_kg
routes$space_time_yield_kg_m3_h <- routes$actual_product_kg / (routes$reactor_volume_m3 * routes$batch_or_residence_time_h)

route_metrics <- routes[, c(
  "route_id",
  "process_type",
  "yield_fraction",
  "e_factor",
  "solvent_intensity",
  "energy_intensity_kWh_kg",
  "space_time_yield_kg_m3_h",
  "hazard_score",
  "separation_difficulty_score"
)]

hazards$residual_risk_proxy <- hazards$severity_score * hazards$likelihood_score * (1 - hazards$safeguard_score)

hazard_summary <- aggregate(
  residual_risk_proxy ~ route_id,
  data = hazards,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

hazard_summary_clean <- data.frame(
  route_id = hazard_summary$route_id,
  mean_residual_risk_proxy = hazard_summary$residual_risk_proxy[, "mean"],
  max_residual_risk_proxy = hazard_summary$residual_risk_proxy[, "max"],
  hazard_count = hazard_summary$residual_risk_proxy[, "n"]
)

write.csv(batches, file.path(table_dir, "r_industrial_batch_data_processed.csv"), row.names = FALSE)
write.csv(summary_clean, file.path(table_dir, "r_industrial_batch_process_summary.csv"), row.names = FALSE)
write.csv(route_metrics, file.path(table_dir, "r_route_metrics.csv"), row.names = FALSE)
write.csv(hazard_summary_clean, file.path(table_dir, "r_hazard_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_industrial_batch_report.txt"))
cat("Synthetic Industrial Chemistry Batch Report\n")
cat("==========================================\n\n")
cat("Batch process summary:\n")
print(summary_clean)
cat("\nRoute metrics:\n")
print(route_metrics)
cat("\nHazard summary:\n")
print(hazard_summary_clean)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R industrial batch workflow complete.")
