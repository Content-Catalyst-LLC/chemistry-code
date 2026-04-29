# First-order kinetics scaffold.
# Synthetic educational data only.

kinetics <- read.csv(file.path("data", "kinetics_timeseries.csv"))

kinetics$ln_concentration <- log(kinetics$concentration_mM)
fit <- lm(ln_concentration ~ time_s, data = kinetics)

k <- -coef(fit)[["time_s"]]
half_life <- log(2) / k

print(kinetics)
print(summary(fit))
print(paste("k_s_inv:", round(k, 6)))
print(paste("half_life_s:", round(half_life, 6)))
