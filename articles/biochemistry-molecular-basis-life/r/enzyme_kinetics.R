# Michaelis-Menten enzyme kinetics scaffold.
# Synthetic educational examples only.

data <- read.csv(file.path("data", "enzyme_kinetics_cases.csv"))

data$velocity_units <- with(
  data,
  Vmax_units * substrate_mM / (Km_mM + substrate_mM)
)

data$fraction_of_Vmax <- data$velocity_units / data$Vmax_units

print(data)
