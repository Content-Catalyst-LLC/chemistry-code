# Atmospheric chemistry monitoring summary.
# Educational workflow using base R only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  article_dir <- getwd()
} else {
  article_dir <- normalizePath(file.path(dirname(script_path), ".."))
}

data_file <- file.path(article_dir, "data", "atmospheric_monitoring_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

atmosphere <- read.csv(data_file, stringsAsFactors = FALSE)

# Ratio to selected reference or screening benchmark.
atmosphere$ratio_to_reference <- atmosphere$concentration / atmosphere$reference_value
atmosphere$screening_flag <- ifelse(
  atmosphere$ratio_to_reference > 1,
  "above_reference",
  "at_or_below_reference"
)

# Summarize by atmospheric chemical class.
class_summary <- aggregate(
  ratio_to_reference ~ class,
  data = atmosphere,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

class_summary_flat <- data.frame(
  class = class_summary$class,
  mean_ratio_to_reference = class_summary$ratio_to_reference[, "mean"],
  max_ratio_to_reference = class_summary$ratio_to_reference[, "max"],
  n = class_summary$ratio_to_reference[, "n"]
)

# Approximate CO2 radiative forcing.
co2_current <- 423.0
co2_reference <- 280.0
co2_forcing <- 5.35 * log(co2_current / co2_reference)

# Count above-reference observations by class.
exceedance_table <- as.data.frame(table(atmosphere$class, atmosphere$screening_flag))
names(exceedance_table) <- c("class", "screening_flag", "count")

write.csv(
  atmosphere,
  file.path(table_dir, "r_screened_atmospheric_data.csv"),
  row.names = FALSE
)

write.csv(
  class_summary_flat,
  file.path(table_dir, "r_atmospheric_class_summary.csv"),
  row.names = FALSE
)

write.csv(
  exceedance_table,
  file.path(table_dir, "r_atmospheric_screening_counts.csv"),
  row.names = FALSE
)

report_lines <- c(
  "# R Atmospheric Monitoring Summary",
  "",
  paste("Total records:", nrow(atmosphere)),
  paste("Records above selected reference:", sum(atmosphere$ratio_to_reference > 1)),
  paste("Approximate CO2 forcing relative to 280 ppm:", round(co2_forcing, 2), "W/m2"),
  "",
  "This educational workflow demonstrates reproducible atmospheric chemistry screening, not compliance assessment."
)

writeLines(report_lines, file.path(report_dir, "r_atmospheric_monitoring_summary.md"))

print(atmosphere)
print(class_summary_flat)
print(exceedance_table)
print(paste("Approximate CO2 forcing:", round(co2_forcing, 2), "W/m2"))
