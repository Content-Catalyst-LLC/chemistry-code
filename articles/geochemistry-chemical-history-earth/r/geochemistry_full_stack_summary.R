# Geochemistry and the Chemical History of Earth
# R rock type, tectonic setting, isotope, and weathering summary.
# Synthetic educational code only.

sample_id <- c("GEOFS001", "GEOFS002", "GEOFS003", "GEOFS004", "GEOFS005", "GEOFS006", "GEOFS007", "GEOFS008")
province <- c("Superior_Craton", "Mid_Ocean_Ridge", "Deccan_Province", "Barberton_Greenstone", "Himalayan_Foreland", "Banded_Iron_Formation", "Andean_Arc", "Siberian_Platform")
rock_type <- c("granite", "basalt", "flood_basalt", "komatiite", "shale", "iron_formation", "andesite", "carbonate")
tectonic_setting <- c("continental_crust", "oceanic_crust", "large_igneous_province", "archean_mantle", "sedimentary_basin", "precambrian_ocean", "subduction_arc", "marine_sedimentary")
sio2 <- c(72.5, 50.2, 49.1, 44.0, 61.0, 38.0, 60.0, 5.5)
al2o3 <- c(14.1, 15.4, 14.8, 7.5, 18.5, 2.5, 17.2, 0.9)
cao <- c(1.8, 11.8, 10.4, 8.9, 1.1, 3.2, 6.1, 51.5)
na2o <- c(3.4, 2.8, 2.4, 0.4, 0.8, 0.1, 3.5, 0.1)
k2o <- c(4.8, 0.3, 0.8, 0.1, 3.6, 0.05, 1.9, 0.05)
mgo <- c(0.6, 7.6, 6.8, 28.0, 2.2, 2.8, 3.5, 1.2)
feo <- c(1.9, 8.9, 10.5, 9.6, 6.5, 42.0, 5.2, 0.5)
tio2 <- c(0.31, 1.7, 2.2, 0.3, 0.9, 0.2, 1.0, 0.03)
epsilon_nd <- c(-6.2, 8.1, 1.5, 4.5, -10.5, -1.0, 2.4, -3.0)
initial_sr_ratio <- c(0.7125, 0.7028, 0.7055, 0.7015, 0.7190, 0.7040, 0.7068, 0.7080)
redox_proxy <- c(0.32, 0.55, 0.48, 0.62, 0.28, 0.92, 0.58, 0.44)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

CIA <- 100 * al2o3 / (al2o3 + cao + na2o + k2o)
mafic_index <- (mgo + feo + tio2) / (mgo + feo + tio2 + sio2)

crustal_evolution_proxy <- clamp01(
  0.35 * clamp01((sio2 - 45) / 30) +
  0.25 * clamp01((initial_sr_ratio - 0.703) / 0.020) +
  0.20 * clamp01((-epsilon_nd + 5) / 15) +
  0.20 * clamp01(k2o / 5)
)

redox_state_proxy <- clamp01(
  0.65 * redox_proxy +
  0.25 * clamp01(feo / 15) +
  0.10 * clamp01(tio2 / 2)
)

geochemical_pressure <- clamp01(
  0.22 * clamp01((CIA - 50) / 50) +
  0.18 * mafic_index +
  0.24 * crustal_evolution_proxy +
  0.24 * redox_state_proxy +
  0.12 * clamp01(abs(epsilon_nd) / 12)
)

data <- data.frame(
  sample_id,
  province,
  rock_type,
  tectonic_setting,
  sio2,
  CIA,
  mafic_index,
  epsilon_nd,
  initial_sr_ratio,
  redox_state_proxy,
  crustal_evolution_proxy,
  geochemical_pressure
)

rock_summary <- aggregate(
  cbind(CIA, mafic_index, redox_state_proxy, crustal_evolution_proxy, geochemical_pressure) ~ rock_type,
  data = data,
  FUN = mean
)

tectonic_summary <- aggregate(
  cbind(CIA, mafic_index, redox_state_proxy, geochemical_pressure) ~ tectonic_setting,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_geochemistry_indicators.csv", row.names = FALSE)
write.csv(rock_summary, "../outputs/tables/r_full_stack_geochemistry_rock_summary.csv", row.names = FALSE)
write.csv(tectonic_summary, "../outputs/tables/r_full_stack_geochemistry_tectonic_summary.csv", row.names = FALSE)

print(rock_summary)
print(tectonic_summary)
