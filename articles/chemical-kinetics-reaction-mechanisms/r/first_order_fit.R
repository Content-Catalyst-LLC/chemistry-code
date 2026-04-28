# First-order kinetic fit using synthetic educational data.

data <- read.csv(file.path("data", "first_order_data.csv"))

for (experiment in unique(data$experiment)) {
  subset <- data[data$experiment == experiment, ]
  subset$ln_concentration <- log(subset$concentration_mol_l)

  model <- lm(ln_concentration ~ time_min, data = subset)

  rate_constant <- -coef(model)[["time_min"]]
  half_life <- log(2) / rate_constant

  print(experiment)
  print(summary(model))
  print(paste("k:", round(rate_constant, 6), "per min"))
  print(paste("half-life:", round(half_life, 6), "min"))
}
