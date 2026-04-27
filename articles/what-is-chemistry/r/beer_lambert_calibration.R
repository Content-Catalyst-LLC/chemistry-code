# Beer-Lambert calibration using synthetic educational data.

calibration <- read.csv(file.path("data", "beer_lambert_calibration.csv"))

model <- lm(absorbance ~ concentration_mol_l, data = calibration)

print(summary(model))

unknown_absorbance <- 0.402
estimated_concentration <- (unknown_absorbance - coef(model)[1]) / coef(model)[2]

print(paste("Estimated concentration:", round(estimated_concentration, 4), "mol/L"))
