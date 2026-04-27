# Synthetic uncertainty budget for chemical metrology.

budget <- read.csv(file.path("data", "uncertainty_budget.csv"))

combined_standard_uncertainty <- sqrt(sum(budget$standard_uncertainty^2))
coverage_factor <- 2
expanded_uncertainty <- coverage_factor * combined_standard_uncertainty

budget$variance_contribution <- budget$standard_uncertainty^2
budget$percent_variance_contribution <- 100 * budget$variance_contribution / sum(budget$variance_contribution)

print(budget)
print(paste("Combined standard uncertainty:", round(combined_standard_uncertainty, 6)))
print(paste("Expanded uncertainty:", round(expanded_uncertainty, 6)))
