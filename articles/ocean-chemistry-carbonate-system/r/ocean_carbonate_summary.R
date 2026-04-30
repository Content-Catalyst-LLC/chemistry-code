# Ocean carbonate chemistry monitoring summary.
# Educational workflow using base R only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  article_dir <- getwd()
} else {
  article_dir <- normalizePath(file.path(dirname(script_path), ".."))
}

data_file <- file.path(article_dir, "data", "ocean_carbonate_monitoring_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

ocean <- read.csv(data_file, stringsAsFactors = FALSE)

# Simplified teaching constants only.
K1 <- 10^-6.0
K2 <- 10^-9.1
Ksp_aragonite <- 6.5e-7
Ksp_calcite <- 4.4e-7

carbonate_alpha2 <- function(pH) {
  H <- 10^(-pH)
  denominator <- H^2 + K1 * H + K1 * K2
  return(K1 * K2 / denominator)
}

ocean$alpha_CO3 <- sapply(ocean$pH_total_scale, carbonate_alpha2)
ocean$carbonate_umol_kg <- ocean$alpha_CO3 * ocean$DIC_umol_kg

ocean$omega_aragonite_simplified <- (
  (ocean$calcium_mmol_kg * 1e-3) *
    (ocean$carbonate_umol_kg * 1e-6)
) / Ksp_aragonite

ocean$omega_calcite_simplified <- (
  (ocean$calcium_mmol_kg * 1e-3) *
    (ocean$carbonate_umol_kg * 1e-6)
) / Ksp_calcite

ocean$saturation_flag <- ifelse(
  ocean$omega_aragonite_simplified < 2,
  "low_aragonite_saturation_attention",
  "higher_aragonite_saturation_screen"
)

ocean$co2_flux_proxy_uatm <- ocean$pCO2_uatm - 420
ocean$flux_direction_screen <- ifelse(
  ocean$co2_flux_proxy_uatm > 0,
  "outgassing_potential",
  "uptake_potential"
)

summary_by_type <- aggregate(
  cbind(pH_total_scale, DIC_umol_kg, total_alkalinity_umol_kg, carbonate_umol_kg, omega_aragonite_simplified) ~ water_type,
  data = ocean,
  FUN = mean
)

flag_counts <- as.data.frame(table(ocean$water_type, ocean$saturation_flag))
names(flag_counts) <- c("water_type", "saturation_flag", "count")

write.csv(ocean, file.path(table_dir, "r_ocean_carbonate_indicators.csv"), row.names = FALSE)
write.csv(summary_by_type, file.path(table_dir, "r_ocean_water_type_summary.csv"), row.names = FALSE)
write.csv(flag_counts, file.path(table_dir, "r_saturation_flag_counts.csv"), row.names = FALSE)

report_lines <- c(
  "# R Ocean Carbonate Chemistry Summary",
  "",
  paste("Total records:", nrow(ocean)),
  paste("Low aragonite saturation attention flags:", sum(ocean$saturation_flag == "low_aragonite_saturation_attention")),
  paste("Outgassing-potential screens:", sum(ocean$flux_direction_screen == "outgassing_potential")),
  "",
  "This educational workflow demonstrates reproducible carbonate-system screening, not research-grade carbonate chemistry."
)

writeLines(report_lines, file.path(report_dir, "r_ocean_carbonate_summary.md"))

print(ocean)
print(summary_by_type)
print(flag_counts)
