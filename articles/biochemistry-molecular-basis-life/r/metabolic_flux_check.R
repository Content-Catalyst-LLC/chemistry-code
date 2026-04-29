# Simplified metabolic flux-balance scaffold.
# Synthetic educational network only.

stoich <- read.csv(file.path("data", "stoichiometry.csv"), check.names = FALSE)
rownames(stoich) <- stoich$metabolite
S <- as.matrix(stoich[, -1])

flux_cases <- read.csv(file.path("data", "metabolic_flux_cases.csv"), check.names = FALSE)

for (i in seq_len(nrow(flux_cases))) {
  case <- flux_cases[i, ]
  v <- as.numeric(case[colnames(S)])
  balance <- S %*% v

  print(case$case_id)
  print(balance)
}
