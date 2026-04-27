# Simple uncertainty summary from synthetic components.

components <- read.csv(file.path("data", "uncertainty_components.csv"))

combined_standard_uncertainty <- sqrt(sum(components$standard_uncertainty^2))
expanded_uncertainty <- 2 * combined_standard_uncertainty

print(components)
print(paste("Combined standard uncertainty:", round(combined_standard_uncertainty, 6)))
print(paste("Expanded uncertainty:", round(expanded_uncertainty, 6)))
