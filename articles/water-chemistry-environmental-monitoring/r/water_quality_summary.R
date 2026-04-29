# Water chemistry monitoring summary.
# Educational workflow using base R only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  article_dir <- getwd()
} else {
  article_dir <- normalizePath(file.path(dirname(script_path), ".."))
}

data_file <- file.path(article_dir, "data", "water_quality_monitoring_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

water <- read.csv(data_file, stringsAsFactors = FALSE)

# Screening ratio.
water$ratio_to_benchmark <- water$concentration / water$benchmark
water$screening_flag <- ifelse(
  water$ratio_to_benchmark > 1,
  "exceeds_benchmark",
  "below_benchmark"
)

# pH flag using an illustrative aquatic range.
water$pH_flag <- ifelse(
  water$pH < 6.5 | water$pH > 9.0,
  "outside_illustrative_aquatic_range",
  "within_illustrative_aquatic_range"
)

# Nutrient load:
# kg/day = mg/L * L/s * 0.0864
water$load_kg_day <- NA
nutrient_rows <- water$analyte %in% c("nitrate_as_N", "phosphate_as_P", "total_phosphorus", "ammonia_as_N") &
  water$unit == "mg/L"

water$load_kg_day[nutrient_rows] <-
  water$concentration[nutrient_rows] * water$flow_L_s[nutrient_rows] * 0.0864

# Exceedance counts by medium.
screening_counts <- as.data.frame(table(water$medium, water$screening_flag))
names(screening_counts) <- c("medium", "screening_flag", "count")

# Summary of ratios by medium.
medium_summary <- aggregate(
  ratio_to_benchmark ~ medium,
  data = water,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

medium_summary_flat <- data.frame(
  medium = medium_summary$medium,
  mean_ratio_to_benchmark = medium_summary$ratio_to_benchmark[, "mean"],
  max_ratio_to_benchmark = medium_summary$ratio_to_benchmark[, "max"],
  n = medium_summary$ratio_to_benchmark[, "n"]
)

nutrient_loads <- water[nutrient_rows, c("sample_id", "site", "analyte", "concentration", "unit", "flow_L_s", "load_kg_day")]

write.csv(water, file.path(table_dir, "r_screened_water_quality_data.csv"), row.names = FALSE)
write.csv(screening_counts, file.path(table_dir, "r_screening_counts.csv"), row.names = FALSE)
write.csv(medium_summary_flat, file.path(table_dir, "r_medium_summary.csv"), row.names = FALSE)
write.csv(nutrient_loads, file.path(table_dir, "r_nutrient_loads.csv"), row.names = FALSE)

report_lines <- c(
  "# R Water Quality Monitoring Summary",
  "",
  paste("Total records:", nrow(water)),
  paste("Benchmark exceedances:", sum(water$ratio_to_benchmark > 1)),
  paste("pH values outside illustrative aquatic range:", sum(water$pH_flag == "outside_illustrative_aquatic_range")),
  paste("Nutrient rows with load estimates:", nrow(nutrient_loads)),
  "",
  "This educational workflow demonstrates reproducible water-chemistry screening, not regulatory assessment."
)

writeLines(report_lines, file.path(report_dir, "r_water_quality_summary.md"))

print(water)
print(screening_counts)
print(medium_summary_flat)
print(nutrient_loads)
