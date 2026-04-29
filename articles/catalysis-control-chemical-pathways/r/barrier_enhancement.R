# Barrier lowering and rate enhancement.
# Synthetic educational data only.

R_const <- 8.314462618

cases <- read.csv(file.path("data", "barrier_cases.csv"))

cases$rate_enhancement_estimate <- exp(
  (cases$delta_Ea_kJ_mol * 1000) / (R_const * cases$temperature_K)
)

cases$log10_rate_enhancement <- log10(cases$rate_enhancement_estimate)

print(cases)
