# Target engagement scaffold.
# Synthetic educational examples only.

data <- read.csv(file.path("data", "target_engagement_cases.csv"))

data$target_engagement_fraction <- with(
  data,
  (signal_control - signal_treated) / (signal_control - signal_max)
)

data$target_engagement_fraction <- pmin(pmax(data$target_engagement_fraction, 0), 1)

print(data)
