# Periodic trend models using a small educational element table.

elements <- read.csv(file.path("data", "elements_sample.csv"))

period_two <- elements[elements$period == 2, ]

radius_model <- lm(atomic_radius_pm ~ atomic_number, data = period_two)
ionization_model <- lm(first_ionization_kj_mol ~ atomic_number, data = period_two)

print(period_two[, c("symbol", "atomic_number", "atomic_radius_pm", "first_ionization_kj_mol")])
print(summary(radius_model))
print(summary(ionization_model))
