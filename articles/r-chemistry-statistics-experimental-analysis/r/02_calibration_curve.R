# Calibration curve and unknown concentration estimates.
# Synthetic educational data only.

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(broom)
})

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
standards_path <- file.path(article_dir, "data", "calibration_standards.csv")
unknowns_path <- file.path(article_dir, "data", "unknown_samples.csv")

model_output <- file.path(article_dir, "outputs", "tables", "calibration_model.csv")
unknown_output <- file.path(article_dir, "outputs", "tables", "unknown_concentrations.csv")
combined_output <- file.path(article_dir, "outputs", "tables", "calibration_curve.csv")

dir.create(dirname(combined_output), recursive = TRUE, showWarnings = FALSE)

standards <- read_csv(standards_path, show_col_types = FALSE)
unknowns <- read_csv(unknowns_path, show_col_types = FALSE)

standard_means <- standards |>
  group_by(concentration_mM) |>
  summarise(
    response_mean = mean(response),
    response_sd = sd(response),
    n = n(),
    .groups = "drop"
  )

fit <- lm(response_mean ~ concentration_mM, data = standard_means)

slope <- coef(fit)[["concentration_mM"]]
intercept <- coef(fit)[["(Intercept)"]]

calibration_model <- standard_means |>
  mutate(
    predicted_response = predict(fit),
    residual = response_mean - predicted_response,
    slope = slope,
    intercept = intercept,
    rmse = sqrt(mean(residual^2))
  )

unknown_estimates <- unknowns |>
  mutate(estimated_concentration_mM = (response - intercept) / slope) |>
  group_by(sample_id) |>
  summarise(
    concentration_mean_mM = mean(estimated_concentration_mM),
    concentration_sd_mM = sd(estimated_concentration_mM),
    n = n(),
    concentration_se_mM = concentration_sd_mM / sqrt(n),
    .groups = "drop"
  )

combined <- bind_rows(
  calibration_model |> mutate(table_type = "calibration_model") |> mutate(across(everything(), as.character)),
  unknown_estimates |> mutate(table_type = "unknown_concentrations") |> mutate(across(everything(), as.character))
)

write_csv(calibration_model, model_output)
write_csv(unknown_estimates, unknown_output)
write_csv(combined, combined_output)

print(calibration_model)
print(unknown_estimates)
cat("Saved:", combined_output, "\n")
