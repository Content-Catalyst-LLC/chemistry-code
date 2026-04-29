# Arrhenius kinetics scaffold.
# Synthetic educational examples only.

R_const <- 8.314462618

cases <- read.csv(file.path("data", "arrhenius_cases.csv"))

cases$rate_constant_s_inv <- cases$pre_exponential_s_inv *
  exp(-(cases$activation_energy_kj_mol * 1000) / (R_const * cases$temperature_K))

cases$ln_k <- log(cases$rate_constant_s_inv)

print(cases)
