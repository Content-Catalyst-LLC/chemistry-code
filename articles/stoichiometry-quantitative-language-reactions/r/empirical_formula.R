# Empirical formula from percent composition.
# Assumes a 100 g sample. Synthetic educational data only.

composition <- read.csv(file.path("data", "percent_composition_examples.csv"))

results <- data.frame()

for (case_id in unique(composition$case_id)) {
  subset <- composition[composition$case_id == case_id, ]
  subset$moles <- subset$percent_mass / subset$atomic_mass_g_mol
  subset$ratio <- subset$moles / min(subset$moles)
  subset$rounded_ratio <- round(subset$ratio)
  results <- rbind(results, subset)
}

print(results)
