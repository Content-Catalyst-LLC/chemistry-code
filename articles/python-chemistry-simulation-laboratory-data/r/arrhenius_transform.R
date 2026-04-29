# Arrhenius transformation scaffold.
# Synthetic educational data only.

arrhenius <- read.csv(file.path("data", "arrhenius_rates.csv"))

arrhenius$inverse_temperature <- 1 / arrhenius$temperature_K
arrhenius$ln_rate <- log(arrhenius$rate_constant_s_inv)

fit <- lm(ln_rate ~ inverse_temperature, data = arrhenius)

print(arrhenius)
print(summary(fit))
