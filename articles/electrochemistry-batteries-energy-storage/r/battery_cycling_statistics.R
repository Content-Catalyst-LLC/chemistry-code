#!/usr/bin/env Rscript

# Synthetic battery cycling workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/battery_cycling_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

cycling <- read.csv(file.path(data_dir, "cycling_data.csv"), stringsAsFactors = FALSE)
cells <- read.csv(file.path(data_dir, "cell_candidates.csv"), stringsAsFactors = FALSE)
impedance <- read.csv(file.path(data_dir, "impedance_measurements.csv"), stringsAsFactors = FALSE)

cycling$coulombic_efficiency <- cycling$discharge_capacity_mAh / cycling$charge_capacity_mAh

initial_capacity <- aggregate(
  discharge_capacity_mAh ~ cell_id,
  data = cycling[cycling$cycle_number == min(cycling$cycle_number), ],
  FUN = mean
)

names(initial_capacity)[2] <- "initial_discharge_capacity_mAh"
cycling <- merge(cycling, initial_capacity, by = "cell_id")
cycling$capacity_retention <- cycling$discharge_capacity_mAh / cycling$initial_discharge_capacity_mAh

summary_table <- aggregate(
  cbind(capacity_retention, coulombic_efficiency) ~ cell_id,
  data = cycling,
  FUN = function(x) c(final = tail(x, 1), mean = mean(x))
)

summary_clean <- data.frame(
  cell_id = summary_table$cell_id,
  final_capacity_retention = summary_table$capacity_retention[, "final"],
  mean_capacity_retention = summary_table$capacity_retention[, "mean"],
  final_coulombic_efficiency = summary_table$coulombic_efficiency[, "final"],
  mean_coulombic_efficiency = summary_table$coulombic_efficiency[, "mean"]
)

degradation_slopes <- do.call(
  rbind,
  lapply(split(cycling, cycling$cell_id), function(df) {
    model <- lm(capacity_retention ~ cycle_number, data = df)
    data.frame(
      cell_id = df$cell_id[1],
      retention_slope_per_cycle = coef(model)[2],
      retention_loss_percent_at_final_cycle = 100 * (1 - df$capacity_retention[nrow(df)])
    )
  })
)

summary_clean <- merge(summary_clean, degradation_slopes, by = "cell_id")
summary_clean$degradation_review_required <- (
  summary_clean$final_capacity_retention < 0.90 |
  summary_clean$mean_coulombic_efficiency < 0.995
)

cells$cell_capacity_mAh <- cells$specific_capacity_mAh_g * cells$active_material_mass_g
cells$cell_energy_Wh <- cells$cell_capacity_mAh * cells$nominal_voltage_V / 1000

chemistry_summary <- aggregate(
  cbind(cell_energy_Wh, critical_material_score, safety_review_score) ~ chemistry,
  data = cells,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

chemistry_summary_clean <- data.frame(
  chemistry = chemistry_summary$chemistry,
  mean_cell_energy_Wh = chemistry_summary$cell_energy_Wh[, "mean"],
  max_cell_energy_Wh = chemistry_summary$cell_energy_Wh[, "max"],
  mean_critical_material_score = chemistry_summary$critical_material_score[, "mean"],
  mean_safety_review_score = chemistry_summary$safety_review_score[, "mean"],
  candidate_count = chemistry_summary$cell_energy_Wh[, "n"]
)

impedance_final <- impedance[impedance$cycle_number == max(impedance$cycle_number), ]
impedance_final$impedance_review_required <- (
  impedance_final$charge_transfer_resistance_mOhm > 150 |
  impedance_final$diffusion_tail_score > 0.75
)

write.csv(cycling, file.path(table_dir, "r_battery_cycling_processed.csv"), row.names = FALSE)
write.csv(summary_clean, file.path(table_dir, "r_battery_degradation_summary.csv"), row.names = FALSE)
write.csv(chemistry_summary_clean, file.path(table_dir, "r_chemistry_summary.csv"), row.names = FALSE)
write.csv(impedance_final, file.path(table_dir, "r_final_impedance_review.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_battery_cycling_report.txt"))
cat("Synthetic Electrochemistry and Energy Storage Report\n")
cat("==================================================\n\n")
cat("Battery degradation summary:\n")
print(summary_clean)
cat("\nChemistry summary:\n")
print(chemistry_summary_clean)
cat("\nFinal impedance review:\n")
print(impedance_final)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R battery cycling workflow complete.")
