# Atmospheric Chemistry and Climate Processes
# R greenhouse gas, aerosol, ozone, and reactive-species summary.
# Synthetic educational code only.

station <- c("Global-CO2", "Global-CH4", "Global-N2O", "Urban-O3", "Urban-NO2", "Wildfire-PM", "Dust-AOD", "Marine-DMS")
chemical_class <- c("greenhouse_gas", "greenhouse_gas", "greenhouse_gas", "secondary_pollutant", "reactive_nitrogen", "aerosol", "aerosol", "sulfur_chemistry")
species <- c("CO2", "CH4", "N2O", "O3", "NO2", "PM2.5", "coarse_aerosol", "DMS")
reference_ratio <- c(423/280, 1950/722, 337/270, 0.078/0.070, 42/53, 38/15, 120/100, 0.45/0.20)
forcing_proxy <- c(5.35 * log(423/280), 0.036 * (sqrt(1950) - sqrt(722)), 0.12 * (sqrt(337) - sqrt(270)), 0, 0, 0, 0, 0)
ozone_index <- c(0, 0, 0, sqrt(38 * 85) * 1.15, sqrt(42 * 60) * 1.05, sqrt(22 * 95) * 0.75, sqrt(5 * 10) * 1.10, sqrt(2 * 8) * 0.90)
aod <- c(0.04, 0.03, 0.03, 0.08, 0.07, 0.68, 0.82, 0.12)
ssa <- c(0.96, 0.95, 0.95, 0.93, 0.92, 0.86, 0.91, 0.97)
lifetime_days <- c(36500, 4380, 43800, 0.20, 0.25, 5, 7, 1)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

aerosol_effect <- -25 * aod * ssa + 12 * aod * (1 - ssa)
persistence_factor <- lifetime_days / (lifetime_days + 30)

pressure_index <- clamp01(
  0.24 * clamp01(log1p(reference_ratio) / log(4)) +
  0.26 * clamp01(abs(forcing_proxy) / 4) +
  0.20 * clamp01(ozone_index / 100) +
  0.18 * clamp01(abs(aerosol_effect) / 20) +
  0.12 * persistence_factor
)

data <- data.frame(
  station,
  chemical_class,
  species,
  reference_ratio,
  forcing_proxy,
  ozone_index,
  aerosol_effect,
  persistence_factor,
  pressure_index
)

class_summary <- aggregate(
  cbind(reference_ratio, forcing_proxy, ozone_index, aerosol_effect, persistence_factor, pressure_index) ~ chemical_class,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_atmospheric_indicators.csv", row.names = FALSE)
write.csv(class_summary, "../outputs/tables/r_full_stack_atmospheric_class_summary.csv", row.names = FALSE)

print(class_summary)
