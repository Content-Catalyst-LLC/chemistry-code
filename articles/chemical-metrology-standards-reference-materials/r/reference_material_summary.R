# Synthetic reference material summary.

materials <- read.csv(file.path("data", "reference_materials.csv"))

materials$relative_expanded_uncertainty_percent <-
  100 * materials$expanded_uncertainty / abs(materials$certified_value)

print(materials)
