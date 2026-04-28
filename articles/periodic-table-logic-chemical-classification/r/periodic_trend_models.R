# Simplified periodic trend models.

elements <- read.csv(file.path("data", "elements_classification.csv"))

for (p in unique(elements$period)) {
  subset <- elements[elements$period == p, ]

  if (nrow(subset) >= 4) {
    radius_model <- lm(atomic_radius_pm ~ atomic_number, data = subset)
    ionization_model <- lm(first_ionization_kj_mol ~ atomic_number, data = subset)

    print(paste("Period", p))
    print(summary(radius_model))
    print(summary(ionization_model))
  }
}
