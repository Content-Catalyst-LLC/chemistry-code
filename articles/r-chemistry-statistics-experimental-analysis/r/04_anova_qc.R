# ANOVA-ready experimental analysis and quality-control summary.
# Synthetic educational data only.

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(broom)
})

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
design_path <- file.path(article_dir, "data", "experimental_design.csv")
qc_path <- file.path(article_dir, "data", "qc_samples.csv")

anova_output <- file.path(article_dir, "outputs", "tables", "anova_summary.csv")
qc_output <- file.path(article_dir, "outputs", "tables", "qc_summary.csv")
combined_output <- file.path(article_dir, "outputs", "tables", "anova_qc.csv")

dir.create(dirname(combined_output), recursive = TRUE, showWarnings = FALSE)

design <- read_csv(design_path, show_col_types = FALSE)

fit <- lm(yield_percent ~ temperature_level * catalyst_loading + solvent, data = design)
anova_summary <- broom::tidy(anova(fit))

qc <- read_csv(qc_path, show_col_types = FALSE) |>
  mutate(
    recovery_percent = 100 * measured_mM / expected_mM,
    bias_mM = measured_mM - expected_mM
  ) |>
  group_by(control_type) |>
  summarise(
    expected_mM = mean(expected_mM),
    mean_measured_mM = mean(measured_mM),
    sd_measured_mM = sd(measured_mM),
    mean_recovery_percent = mean(recovery_percent),
    mean_bias_mM = mean(bias_mM),
    n = n(),
    .groups = "drop"
  )

combined <- bind_rows(
  anova_summary |> mutate(table_type = "anova_summary") |> mutate(across(everything(), as.character)),
  qc |> mutate(table_type = "qc_summary") |> mutate(across(everything(), as.character))
)

write_csv(anova_summary, anova_output)
write_csv(qc, qc_output)
write_csv(combined, combined_output)

print(anova_summary)
print(qc)
cat("Saved:", combined_output, "\n")
