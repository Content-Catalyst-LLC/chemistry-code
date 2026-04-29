# Boltzmann conformer population scaffold.
# Synthetic educational examples only.

R_const <- 8.314462618
data <- read.csv(file.path("data", "conformer_energies.csv"))

result <- data.frame()

for (mol in unique(data$molecule)) {
  subset_data <- data[data$molecule == mol, ]
  T <- subset_data$temperature_K[1]
  weights <- exp(-(subset_data$relative_energy_kj_mol * 1000) / (R_const * T))
  subset_data$boltzmann_weight <- weights
  subset_data$population <- weights / sum(weights)
  result <- rbind(result, subset_data)
}

print(result)
