# Gibbs free energy and equilibrium constants.

R_gas_constant <- 8.314462618

gibbs <- read.csv(file.path("data", "gibbs_examples.csv"))

gibbs$delta_g_standard_kj_mol <- gibbs$delta_h_kj_mol -
  gibbs$temperature_k * gibbs$delta_s_j_mol_k / 1000

gibbs$equilibrium_constant <- exp(
  -(gibbs$delta_g_standard_kj_mol * 1000) /
    (R_gas_constant * gibbs$temperature_k)
)

gibbs$delta_g_nonstandard_kj_mol <- gibbs$delta_g_standard_kj_mol +
  (R_gas_constant * gibbs$temperature_k * log(gibbs$reaction_quotient)) / 1000

print(gibbs)
