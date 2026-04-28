# Clausius-Clapeyron-style vapor pressure fit.
# Synthetic educational data only.

vapor <- read.csv(file.path("data", "vapor_pressure_sample.csv"))

vapor$inverse_temperature_K_inv <- 1 / vapor$temperature_K
vapor$ln_pressure_kPa <- log(vapor$pressure_kPa)

model <- lm(ln_pressure_kPa ~ inverse_temperature_K_inv, data = vapor)

slope <- coef(model)[["inverse_temperature_K_inv"]]
R_gas_constant <- 8.314462618
estimated_delta_h_vap_kj_mol <- (-slope * R_gas_constant) / 1000

print(vapor)
print(summary(model))
print(paste("Estimated Delta H vap:", round(estimated_delta_h_vap_kj_mol, 4), "kJ/mol"))
