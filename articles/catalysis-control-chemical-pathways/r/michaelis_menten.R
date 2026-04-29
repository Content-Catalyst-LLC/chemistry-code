# Michaelis-Menten catalytic saturation.
# Synthetic educational data only.

enzyme <- read.csv(file.path("data", "enzyme_cases.csv"))

enzyme$rate_umol_min <- (enzyme$Vmax_umol_min * enzyme$substrate_mM) /
  (enzyme$Km_mM + enzyme$substrate_mM)

enzyme$fraction_of_vmax <- enzyme$rate_umol_min / enzyme$Vmax_umol_min

print(enzyme)
