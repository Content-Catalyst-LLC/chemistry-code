# Environmental chemistry monitoring summary
# Educational workflow using base R only.

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_file <- file.path(article_dir, "data", "environmental_monitoring_synthetic.csv")
table_dir <- file.path(article_dir, "outputs", "tables")
report_dir <- file.path(article_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

monitoring <- read.csv(data_file, stringsAsFactors = FALSE)

# Compute a benchmark screening ratio.
monitoring$hazard_quotient <- monitoring$concentration / monitoring$benchmark
monitoring$screening_flag <- ifelse(
  monitoring$hazard_quotient > 1,
  "exceeds_benchmark",
  "below_benchmark"
)

# Aggregate by medium.
medium_summary <- aggregate(
  hazard_quotient ~ medium,
  data = monitoring,
  FUN = function(x) c(mean = mean(x), max = max(x), n = length(x))
)

# Flatten aggregate columns for easier export.
medium_summary_flat <- data.frame(
  medium = medium_summary$medium,
  mean_hazard_quotient = medium_summary$hazard_quotient[, "mean"],
  max_hazard_quotient = medium_summary$hazard_quotient[, "max"],
  n = medium_summary$hazard_quotient[, "n"]
)

# Exceedance count by medium.
exceedance_table <- as.data.frame(table(monitoring$medium, monitoring$screening_flag))
names(exceedance_table) <- c("medium", "screening_flag", "count")

write.csv(
  monitoring,
  file.path(table_dir, "r_screened_monitoring_data.csv"),
  row.names = FALSE
)

write.csv(
  medium_summary_flat,
  file.path(table_dir, "r_medium_summary.csv"),
  row.names = FALSE
)

write.csv(
  exceedance_table,
  file.path(table_dir, "r_exceedance_counts.csv"),
  row.names = FALSE
)

report_lines <- c(
  "# R Environmental Monitoring Summary",
  "",
  paste("Total records:", nrow(monitoring)),
  paste("Benchmark exceedances:", sum(monitoring$hazard_quotient > 1)),
  "",
  "This educational workflow demonstrates reproducible screening, not regulatory assessment."
)

writeLines(report_lines, file.path(report_dir, "r_environmental_monitoring_summary.md"))

print(monitoring)
print(medium_summary_flat)
print(exceedance_table)
