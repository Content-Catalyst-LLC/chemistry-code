# Linear calibration curve using synthetic educational data.

calibration <- read.csv(file.path("data", "calibration_curve.csv"))
unknowns <- read.csv(file.path("data", "unknown_samples.csv"))

model <- lm(instrument_response ~ concentration_mol_l, data = calibration)

slope <- coef(model)[2]
intercept <- coef(model)[1]

unknowns$estimated_concentration_mol_l <- (unknowns$instrument_response - intercept) / slope

print(summary(model))
print(round(unknowns, 6))
