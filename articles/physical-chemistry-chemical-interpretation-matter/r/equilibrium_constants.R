# Equilibrium constants from standard Gibbs free energy.
# Synthetic educational examples only.

R_const <- 8.314462618

cases <- read.csv(file.path("data", "thermodynamic_cases.csv"))

cases$K <- exp(-(cases$delta_g_standard_kj_mol * 1000) / (R_const * cases$temperature_K))
cases$log10_K <- log10(cases$K)
cases$delta_g_kj_mol <- cases$delta_g_standard_kj_mol +
  (R_const * cases$temperature_K * log(cases$reaction_quotient)) / 1000

print(cases)
