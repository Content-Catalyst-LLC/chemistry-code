# Replicate precision and uncertainty using synthetic data.

measurements <- read.csv(file.path("data", "replicate_measurements.csv"))

mean_mass <- mean(measurements$measured_mass_g)
sd_mass <- sd(measurements$measured_mass_g)
rsd_percent <- 100 * sd_mass / mean_mass
standard_uncertainty <- sd_mass / sqrt(nrow(measurements))
expanded_uncertainty <- 2 * standard_uncertainty

summary_table <- data.frame(
  sample = unique(measurements$sample),
  n_replicates = nrow(measurements),
  mean_mass_g = mean_mass,
  standard_deviation_g = sd_mass,
  rsd_percent = rsd_percent,
  coverage_factor_k = 2,
  expanded_uncertainty_g = expanded_uncertainty
)

print(round(summary_table, 8))
