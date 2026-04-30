# Astrochemistry and the Molecular Universe
# R molecular-cloud, disk, comet, ice, and interstellar chemistry summary.
# Synthetic educational code only.

record_id <- c("ASTFS001", "ASTFS002", "ASTFS003", "ASTFS004", "ASTFS005", "ASTFS006", "ASTFS007", "ASTFS008")
region <- c("Taurus_TMC1", "Orion_KL", "TW_Hya", "Comet_67P", "Titan", "Europa_Surface_Ice", "Sgr_B2_N", "Diffuse_Cloud")
environment <- c("cold_dark_cloud", "hot_core", "disk_midplane", "cometary_coma", "planetary_atmosphere", "icy_world", "hot_core", "translucent_cloud")
molecular_family <- c("carbon_chain", "complex_organic", "ice_chemistry", "volatile_ice", "nitrile", "oxidant_ice", "complex_organic", "small_molecule")
species <- c("HC3N", "CH3OCH3", "H2O_ice", "CO", "HCN", "H2O2", "CH3OH", "CH")
density <- c(1.2e5, 5.0e6, 1.0e8, 1.0e5, 1.0e7, 1.0e4, 3.0e6, 8.0e2)
column_density <- c(2.2e13, 8.0e15, 1.0e18, 4.5e16, 3.0e15, 8.0e14, 2.5e17, 1.5e13)
uv_field <- c(0.05, 10.0, 0.20, 1.00, 3.00, 0.80, 20.0, 5.00)
cosmic_ray <- c(1.3e-17, 5.0e-16, 1.0e-17, 1.0e-17, 2.0e-16, 8.0e-16, 6.0e-16, 3.0e-17)
visual_extinction <- c(12.0, 8.0, 20.0, 1.0, 0.5, 0.2, 10.0, 1.2)
ice_fraction <- c(0.72, 0.35, 0.88, 0.60, 0.15, 0.78, 0.42, 0.10)
water_ice_index <- c(0.65, 0.42, 0.95, 0.50, 0.12, 0.90, 0.58, 0.05)
organic_complexity <- c(0.54, 0.92, 0.30, 0.48, 0.72, 0.24, 0.86, 0.22)
deuteration <- c(0.08, 0.03, 0.12, 0.04, 0.02, 0.01, 0.05, 0.01)
metallicity <- c(1.00, 1.15, 1.00, 1.00, 0.95, 1.00, 1.20, 0.85)
qc_score <- c(0.93, 0.90, 0.91, 0.88, 0.86, 0.84, 0.89, 0.87)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

uv_attenuation <- uv_field * exp(-1.8 * visual_extinction)
ionization_pressure <- clamp01(log10(pmax(cosmic_ray, 1e-20) / 1e-18) / 4)
column_component <- clamp01(log10(pmax(column_density, 1)) / 18)

molecular_complexity_score <- clamp01(
  0.45 * organic_complexity +
  0.35 * column_component +
  0.20 * metallicity
)

ice_chemistry_score <- clamp01(
  0.45 * ice_fraction +
  0.35 * water_ice_index +
  0.20 * clamp01(log10(pmax(density, 1)) / 8)
)

activity_index <- clamp01(
  0.24 * molecular_complexity_score +
  0.22 * ice_chemistry_score +
  0.18 * ionization_pressure +
  0.12 * deuteration +
  0.08 * clamp01(uv_attenuation / 10) +
  0.06 * (1 - qc_score)
)

data <- data.frame(
  record_id,
  region,
  environment,
  molecular_family,
  species,
  density,
  column_density,
  uv_attenuation,
  ionization_pressure,
  molecular_complexity_score,
  ice_chemistry_score,
  deuteration,
  activity_index
)

environment_summary <- aggregate(
  cbind(molecular_complexity_score, ice_chemistry_score, ionization_pressure, activity_index) ~ environment,
  data = data,
  FUN = mean
)

family_summary <- aggregate(
  cbind(molecular_complexity_score, ice_chemistry_score, activity_index) ~ molecular_family,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_astrochemistry_indicators.csv", row.names = FALSE)
write.csv(environment_summary, "../outputs/tables/r_full_stack_astrochemistry_environment_summary.csv", row.names = FALSE)
write.csv(family_summary, "../outputs/tables/r_full_stack_astrochemistry_family_summary.csv", row.names = FALSE)

print(environment_summary)
print(family_summary)
