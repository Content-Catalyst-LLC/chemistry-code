# van 't Hoff-style fit using synthetic equilibrium data.

R_gas_constant <- 8.314462618

equilibrium <- read.csv(file.path("data", "vant_hoff_examples.csv"))

equilibrium$inverse_temperature <- 1 / equilibrium$temperature_k
equilibrium$ln_k <- log(equilibrium$equilibrium_constant)

model <- lm(ln_k ~ inverse_temperature, data = equilibrium)

slope <- coef(model)[["inverse_temperature"]]
intercept <- coef(model)[["(Intercept)"]]

delta_h_standard_j_mol <- -slope * R_gas_constant
delta_s_standard_j_mol_k <- intercept * R_gas_constant

print(equilibrium)
print(summary(model))
print(paste("Estimated Delta H:", round(delta_h_standard_j_mol / 1000, 4), "kJ/mol"))
print(paste("Estimated Delta S:", round(delta_s_standard_j_mol_k, 4), "J/mol K"))
