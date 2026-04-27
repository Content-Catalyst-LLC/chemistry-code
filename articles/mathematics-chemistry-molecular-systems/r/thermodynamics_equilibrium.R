# Thermodynamic relationship between standard free energy and equilibrium constant.

R <- 8.314462618
thermo <- read.csv(file.path("data", "thermodynamics_examples.csv"))

thermo$equilibrium_constant_K <- exp(
  -(thermo$delta_g_standard_kj_mol * 1000) / (R * thermo$temperature_k)
)

print(thermo)
