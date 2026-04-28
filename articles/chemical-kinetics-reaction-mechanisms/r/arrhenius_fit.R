# Arrhenius activation-energy estimate using synthetic educational data.

R_gas_constant <- 8.314462618

data <- read.csv(file.path("data", "arrhenius_data.csv"))

for (reaction in unique(data$reaction)) {
  subset <- data[data$reaction == reaction, ]

  subset$inverse_temperature <- 1 / subset$temperature_K
  subset$ln_k <- log(subset$rate_constant_s_inv)

  model <- lm(ln_k ~ inverse_temperature, data = subset)

  slope <- coef(model)[["inverse_temperature"]]
  intercept <- coef(model)[["(Intercept)"]]

  activation_energy_kj_mol <- (-slope * R_gas_constant) / 1000
  pre_exponential_factor <- exp(intercept)

  print(reaction)
  print(summary(model))
  print(paste("Ea:", round(activation_energy_kj_mol, 4), "kJ/mol"))
  print(paste("A:", signif(pre_exponential_factor, 5), "s^-1"))
}
