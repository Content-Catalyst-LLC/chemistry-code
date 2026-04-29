# First-order kinetics and Arrhenius analysis.
# Synthetic educational data only.

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
kinetics_path <- file.path(article_dir, "data", "kinetics_timeseries.csv")
arrhenius_path <- file.path(article_dir, "data", "arrhenius_rates.csv")

kinetics_output <- file.path(article_dir, "outputs", "tables", "first_order_kinetics.csv")
arrhenius_output <- file.path(article_dir, "outputs", "tables", "arrhenius_transform.csv")
combined_output <- file.path(article_dir, "outputs", "tables", "kinetics_arrhenius.csv")

dir.create(dirname(combined_output), recursive = TRUE, showWarnings = FALSE)

kinetics <- read_csv(kinetics_path, show_col_types = FALSE) |>
  mutate(ln_concentration = log(concentration_mM))

kinetics_fit <- lm(ln_concentration ~ time_s, data = kinetics)
k <- -coef(kinetics_fit)[["time_s"]]
half_life_s <- log(2) / k

kinetics_result <- kinetics |>
  mutate(
    predicted_ln_concentration = predict(kinetics_fit),
    predicted_concentration_mM = exp(predicted_ln_concentration),
    residual_mM = concentration_mM - predicted_concentration_mM,
    k_s_inv = k,
    half_life_s = half_life_s
  )

arrhenius <- read_csv(arrhenius_path, show_col_types = FALSE) |>
  mutate(
    inverse_temperature_K_inv = 1 / temperature_K,
    ln_rate_constant = log(rate_constant_s_inv)
  )

arrhenius_fit <- lm(ln_rate_constant ~ inverse_temperature_K_inv, data = arrhenius)
R_j_mol_k <- 8.314462618
activation_energy_J_mol <- -coef(arrhenius_fit)[["inverse_temperature_K_inv"]] * R_j_mol_k

arrhenius_result <- arrhenius |>
  mutate(
    arrhenius_slope = coef(arrhenius_fit)[["inverse_temperature_K_inv"]],
    arrhenius_intercept = coef(arrhenius_fit)[["(Intercept)"]],
    activation_energy_J_mol_estimate = activation_energy_J_mol
  )

combined <- bind_rows(
  kinetics_result |> mutate(table_type = "first_order_kinetics") |> mutate(across(everything(), as.character)),
  arrhenius_result |> mutate(table_type = "arrhenius_transform") |> mutate(across(everything(), as.character))
)

write_csv(kinetics_result, kinetics_output)
write_csv(arrhenius_result, arrhenius_output)
write_csv(combined, combined_output)

print(kinetics_result)
print(arrhenius_result)
cat("Saved:", combined_output, "\n")
