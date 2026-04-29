# Soil chemistry monitoring summary.
# Educational workflow using base R only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  article_dir <- getwd()
} else {
  article_dir <- normalizePath(file.path(dirname(script_path), ".."))
}

data_file <- file.path(article_dir, "data", "soil_monitoring_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

soil <- read.csv(data_file, stringsAsFactors = FALSE)

# Soil organic carbon stock approximation:
# Mg C/ha = SOC_percent * bulk density * depth_cm
soil$soc_stock_Mg_ha <- soil$soil_organic_carbon_percent *
  soil$bulk_density_g_cm3 *
  soil$depth_cm

# Base saturation.
soil$base_saturation_percent <- 100 *
  soil$base_cations_cmolc_kg / soil$cec_cmolc_kg

# Screening flags.
soil$pH_flag <- ifelse(soil$pH < 5.8, "acidic_screen", "not_acidic_screen")
soil$salinity_flag <- ifelse(
  soil$electrical_conductivity_dS_m > 1.2,
  "elevated_salinity_screen",
  "not_elevated_screen"
)
soil$phosphorus_flag <- ifelse(
  soil$phosphorus_mg_kg > 60,
  "high_phosphorus_runoff_attention",
  "not_high_screen"
)
soil$nitrate_flag <- ifelse(
  soil$nitrate_mg_kg > 30,
  "high_nitrate_leaching_attention",
  "not_high_screen"
)

# Summarize by land use.
land_use_summary <- aggregate(
  cbind(pH, soil_organic_carbon_percent, soc_stock_Mg_ha, cec_cmolc_kg) ~ land_use,
  data = soil,
  FUN = mean
)

# Nitrogen balance examples.
nitrogen_balance <- data.frame(
  field = c("Field-A", "Field-B"),
  fertilizer_N_kg_ha = c(135, 165),
  manure_N_kg_ha = c(0, 35),
  fixation_N_kg_ha = c(25, 20),
  harvest_removal_N_kg_ha = c(118, 145),
  leaching_loss_N_kg_ha = c(18, 28),
  gaseous_loss_N_kg_ha = c(12, 22)
)

nitrogen_balance$net_N_kg_ha <- with(
  nitrogen_balance,
  fertilizer_N_kg_ha +
    manure_N_kg_ha +
    fixation_N_kg_ha -
    harvest_removal_N_kg_ha -
    leaching_loss_N_kg_ha -
    gaseous_loss_N_kg_ha
)

write.csv(soil, file.path(table_dir, "r_screened_soil_monitoring_data.csv"), row.names = FALSE)
write.csv(land_use_summary, file.path(table_dir, "r_land_use_summary.csv"), row.names = FALSE)
write.csv(nitrogen_balance, file.path(table_dir, "r_nitrogen_balance_examples.csv"), row.names = FALSE)

report_lines <- c(
  "# R Soil Chemistry Monitoring Summary",
  "",
  paste("Total samples:", nrow(soil)),
  paste("Acidic screen flags:", sum(soil$pH_flag == "acidic_screen")),
  paste("High phosphorus flags:", sum(soil$phosphorus_flag == "high_phosphorus_runoff_attention")),
  paste("High nitrate flags:", sum(soil$nitrate_flag == "high_nitrate_leaching_attention")),
  "",
  "This educational workflow demonstrates reproducible soil-chemistry screening, not agronomic or regulatory assessment."
)

writeLines(report_lines, file.path(report_dir, "r_soil_monitoring_summary.md"))

print(soil)
print(land_use_summary)
print(nitrogen_balance)
