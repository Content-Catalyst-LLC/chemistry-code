# Geochemical data summary.
# Educational workflow using base R only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  article_dir <- getwd()
} else {
  article_dir <- normalizePath(file.path(dirname(script_path), ".."))
}

data_file <- file.path(article_dir, "data", "geochemical_samples_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

geo <- read.csv(data_file, stringsAsFactors = FALSE)

# Simplified Chemical Index of Alteration.
# Teaching-only version: uses weight percentages and does not correct CaO*.
geo$CIA_simplified <- 100 * geo$Al2O3_wt_pct /
  (geo$Al2O3_wt_pct + geo$CaO_wt_pct + geo$Na2O_wt_pct + geo$K2O_wt_pct)

geo$weathering_screen <- ifelse(
  geo$CIA_simplified > 80,
  "strong_weathering_screen",
  "moderate_or_low_screen"
)

# Trace-element ratios.
geo$Rb_Sr_ratio <- geo$Rb_ppm / geo$Sr_ppm
geo$Th_U_ratio <- geo$Th_ppm / geo$U_ppm
geo$Zr_Y_ratio <- geo$Zr_ppm / geo$Y_ppm

# Simplified parent-daughter radiometric age.
decay_constant <- 1.55125e-10
geo$radiometric_age_Ma_simplified <- (1 / decay_constant) *
  log(1 + geo$radiogenic_daughter_units / geo$parent_isotope_units) / 1e6

summary_by_type <- aggregate(
  cbind(SiO2_wt_pct, CIA_simplified, Rb_Sr_ratio, Zr_Y_ratio, radiometric_age_Ma_simplified) ~ rock_type,
  data = geo,
  FUN = mean
)

write.csv(geo, file.path(table_dir, "r_geochemical_indicators.csv"), row.names = FALSE)
write.csv(summary_by_type, file.path(table_dir, "r_rock_type_summary.csv"), row.names = FALSE)

report_lines <- c(
  "# R Geochemical Summary",
  "",
  paste("Total samples:", nrow(geo)),
  paste("Strong weathering screens:", sum(geo$weathering_screen == "strong_weathering_screen")),
  "",
  "This educational workflow demonstrates reproducible geochemical screening, not professional interpretation."
)

writeLines(report_lines, file.path(report_dir, "r_geochemical_summary.md"))

print(geo)
print(summary_by_type)
