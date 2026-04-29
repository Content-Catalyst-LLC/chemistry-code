# Calibration, LOD, and LOQ scaffold.
# Synthetic educational examples only.

standards <- read.csv(file.path("data", "calibration_standards.csv"))
blanks <- read.csv(file.path("data", "blank_signals.csv"))
unknowns <- read.csv(file.path("data", "unknown_samples.csv"))

fit <- lm(signal ~ concentration_mg_L, data = standards)

intercept <- coef(fit)[[1]]
slope <- coef(fit)[[2]]

blank_sd <- sd(blanks$signal)

LOD <- 3 * blank_sd / slope
LOQ <- 10 * blank_sd / slope

unknowns$estimated_concentration_mg_L <- (
  (unknowns$signal - intercept) / slope
) * unknowns$dilution_factor

print(summary(fit))
print(paste("LOD:", round(LOD, 6)))
print(paste("LOQ:", round(LOQ, 6)))
print(unknowns)
