# Dose-response scaffold.
# Synthetic educational examples only.

data <- read.csv(file.path("data", "dose_response_cases.csv"))

data$response_fraction <- with(
  data,
  bottom + (top - bottom) / (1 + (EC50_uM / compound_uM)^hill_slope)
)

print(data)
