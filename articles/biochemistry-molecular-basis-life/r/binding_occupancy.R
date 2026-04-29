# Protein-ligand binding occupancy scaffold.
# Synthetic educational examples only.

data <- read.csv(file.path("data", "binding_cases.csv"))

data$simple_fractional_occupancy <- with(
  data,
  ligand_uM / (Kd_uM + ligand_uM)
)

data$hill_fractional_occupancy <- with(
  data,
  ligand_uM^hill_n / (Kd_uM^hill_n + ligand_uM^hill_n)
)

print(data)
