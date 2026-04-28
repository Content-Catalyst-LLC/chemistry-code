# Michaelis-Menten enzyme kinetics using synthetic educational data.

enzyme <- read.csv(file.path("data", "enzyme_kinetics_data.csv"))

model <- nls(
  rate_umol_min ~ (vmax * substrate_mM) / (km + substrate_mM),
  data = enzyme,
  start = list(vmax = 1.8, km = 0.8)
)

print(enzyme)
print(summary(model))
print(coef(model))
