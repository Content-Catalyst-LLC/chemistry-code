# Astrochemical survey summary.
# Educational workflow using base R only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  article_dir <- getwd()
} else {
  article_dir <- normalizePath(file.path(dirname(script_path), ".."))
}

data_file <- file.path(article_dir, "data", "astrochemical_survey_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

astro <- read.csv(data_file, stringsAsFactors = FALSE)

c_km_s <- 299792.458

astro$radial_velocity_km_s <- -c_km_s *
  (astro$observed_frequency_GHz - astro$rest_frequency_GHz) /
  astro$rest_frequency_GHz

astro$fractional_abundance <- astro$column_density_cm2 / astro$H2_column_density_cm2

astro$thermal_regime <- ifelse(
  astro$dust_temperature_K >= 100,
  "warm_or_hot",
  "cold_or_moderate"
)

astro$photochemical_regime <- ifelse(
  astro$uv_field_index > 10,
  "high_photochemical_processing",
  "lower_photochemical_processing"
)

environment_summary <- aggregate(
  cbind(fractional_abundance, dust_temperature_K, gas_temperature_K, uv_field_index) ~ environment,
  data = astro,
  FUN = mean
)

class_counts <- as.data.frame(table(astro$molecule_class, astro$thermal_regime))
names(class_counts) <- c("molecule_class", "thermal_regime", "count")

photochemical_counts <- as.data.frame(table(astro$environment, astro$photochemical_regime))
names(photochemical_counts) <- c("environment", "photochemical_regime", "count")

write.csv(astro, file.path(table_dir, "r_astrochemical_indicators.csv"), row.names = FALSE)
write.csv(environment_summary, file.path(table_dir, "r_environment_summary.csv"), row.names = FALSE)
write.csv(class_counts, file.path(table_dir, "r_class_counts.csv"), row.names = FALSE)
write.csv(photochemical_counts, file.path(table_dir, "r_photochemical_counts.csv"), row.names = FALSE)

report_lines <- c(
  "# R Astrochemical Survey Summary",
  "",
  paste("Total records:", nrow(astro)),
  paste("High photochemical records:", sum(astro$photochemical_regime == "high_photochemical_processing")),
  paste("Warm or hot records:", sum(astro$thermal_regime == "warm_or_hot")),
  "",
  "This educational workflow demonstrates reproducible astrochemical survey screening, not professional line identification."
)

writeLines(report_lines, file.path(report_dir, "r_astrochemical_survey_summary.md"))

print(astro)
print(environment_summary)
print(class_counts)
print(photochemical_counts)
