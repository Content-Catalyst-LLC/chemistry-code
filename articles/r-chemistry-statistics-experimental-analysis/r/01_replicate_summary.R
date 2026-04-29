# Replicate summary for R chemistry workflow.
# Synthetic educational data only.

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
input_path <- file.path(article_dir, "data", "replicate_measurements.csv")
output_path <- file.path(article_dir, "outputs", "tables", "replicate_summary.csv")

dir.create(dirname(output_path), recursive = TRUE, showWarnings = FALSE)

measurements <- read_csv(input_path, show_col_types = FALSE)

summary_table <- measurements |>
  group_by(sample_id, analyte, method_id, batch_id) |>
  summarise(
    mean_mM = mean(measurement_mM),
    sd_mM = sd(measurement_mM),
    n = n(),
    se_mM = sd_mM / sqrt(n),
    rsd_percent = 100 * sd_mM / mean_mM,
    .groups = "drop"
  )

write_csv(summary_table, output_path)

print(summary_table)
cat("Saved:", output_path, "\n")
