# Simplified pH calculations for synthetic strong-acid examples.

solutions <- read.csv(file.path("data", "ph_examples.csv"))

solutions$pH <- -log10(solutions$hydrogen_concentration_mol_l)

print(round(solutions, 4))
