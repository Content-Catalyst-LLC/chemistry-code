# Ocean Chemistry and the Carbonate System
# R ocean chemistry and acidification summary.
# Synthetic educational code only.

region <- c("North_Atlantic", "Equatorial_Pacific", "Southern_Ocean", "North_Pacific", "Arabian_Sea", "Caribbean_Reef", "California_Current", "Deep_Atlantic")
water_mass <- c("surface_subpolar", "surface_upwelling", "surface_polar", "intermediate_water", "oxygen_minimum_zone", "surface_tropical", "coastal_upwelling", "deep_water")
pH <- c(8.08, 7.92, 8.02, 7.78, 7.62, 8.12, 7.82, 7.74)
alkalinity <- c(2310, 2285, 2325, 2290, 2320, 2380, 2260, 2350)
dic <- c(2060, 2130, 2115, 2220, 2265, 2040, 2185, 2280)
pco2 <- c(415, 520, 430, 780, 1050, 390, 850, 980)
carbonate <- c(185, 145, 165, 85, 62, 210, 95, 70)
calcium <- c(10.3, 10.2, 10.4, 10.1, 10.2, 10.5, 10.0, 10.3)
oxygen <- c(255, 210, 300, 110, 18, 230, 145, 170)
nitrate <- c(6.2, 14.5, 22.0, 34.0, 38.0, 0.4, 28.0, 30.0)
phosphate <- c(0.8, 1.9, 1.6, 2.5, 3.2, 0.2, 2.2, 2.0)
silicate <- c(3, 8, 18, 40, 28, 1, 22, 65)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

alkalinity_dic_ratio <- alkalinity / dic
buffer_proxy <- clamp01(
  0.55 * clamp01((pH - 7.6) / 0.7) +
  0.45 * clamp01((alkalinity_dic_ratio - 1.0) / 0.20)
)

omega_aragonite <- (carbonate * calcium * 1000) / (60 * 100000)

acidification_pressure <- clamp01(
  0.30 * clamp01((8.2 - pH) / 0.7) +
  0.25 * clamp01((pco2 - 400) / 800) +
  0.25 * clamp01((180 - carbonate) / 180) +
  0.20 * clamp01((3 - omega_aragonite) / 3)
)

deoxygenation_pressure <- clamp01((180 - oxygen) / 180)

nutrient_upwelling_index <- clamp01(
  0.40 * clamp01(nitrate / 35) +
  0.30 * clamp01(phosphate / 3) +
  0.30 * clamp01(silicate / 60)
)

carbonate_system_pressure <- clamp01(
  0.36 * acidification_pressure +
  0.20 * deoxygenation_pressure +
  0.16 * nutrient_upwelling_index +
  0.18 * (1 - buffer_proxy)
)

data <- data.frame(
  region,
  water_mass,
  pH,
  alkalinity,
  dic,
  pco2,
  carbonate,
  omega_aragonite,
  alkalinity_dic_ratio,
  buffer_proxy,
  acidification_pressure,
  deoxygenation_pressure,
  nutrient_upwelling_index,
  carbonate_system_pressure
)

water_mass_summary <- aggregate(
  cbind(pH, pco2, carbonate, omega_aragonite, acidification_pressure, deoxygenation_pressure, carbonate_system_pressure) ~ water_mass,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_ocean_indicators.csv", row.names = FALSE)
write.csv(water_mass_summary, "../outputs/tables/r_full_stack_ocean_water_mass_summary.csv", row.names = FALSE)

print(water_mass_summary)
