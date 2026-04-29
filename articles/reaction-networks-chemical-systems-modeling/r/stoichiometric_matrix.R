# Stoichiometric matrix for a small reaction network.
# Synthetic educational data only.

stoich <- read.csv(file.path("data", "stoichiometry.csv"), check.names = FALSE)
rownames(stoich) <- stoich$species_id
matrix_data <- as.matrix(stoich[, -1])

print(matrix_data)
