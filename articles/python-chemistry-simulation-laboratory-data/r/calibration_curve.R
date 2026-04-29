# Calibration curve scaffold.
# Synthetic educational data only.

standards <- read.csv(file.path("data", "calibration_standards.csv"))
unknowns <- read.csv(file.path("data", "unknown_samples.csv"))

standard_means <- aggregate(response ~ concentration_mM, data = standards, mean)
fit <- lm(response ~ concentration_mM, data = standard_means)

slope <- coef(fit)[["concentration_mM"]]
intercept <- coef(fit)[["(Intercept)"]]

unknowns$estimated_concentration_mM <- (unknowns$response - intercept) / slope

print(standard_means)
print(summary(fit))
print(unknowns)
