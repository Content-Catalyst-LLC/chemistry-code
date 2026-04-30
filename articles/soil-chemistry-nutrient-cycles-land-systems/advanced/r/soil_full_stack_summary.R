# Soil Chemistry, Nutrient Cycles, and Land Systems
# R soil class, nutrient pressure, and land-system summary.
# Synthetic educational code only.

site <- c("Prairie-A", "Field-B", "Irrigated-C", "Forest-D", "Degraded-E", "Wetland-F", "Pasture-G")
land_use <- c("cropland", "intensive_cropland", "irrigated_agriculture", "forest", "degraded_land", "wetland", "pasture")
soil_group <- c("mollisol_like", "sandy_low_om", "salinity_risk", "forest_soil", "eroded_low_om", "hydric_soil", "grassland_soil")
pH <- c(6.4, 5.5, 8.2, 5.9, 5.1, 6.8, 6.2)
organic_matter <- c(4.8, 2.1, 1.6, 7.2, 0.9, 8.0, 3.9)
cec <- c(22, 9, 14, 18, 5, 26, 17)
nitrate <- c(18, 42, 25, 4, 8, 6, 15)
ammonium <- c(6, 8, 5, 3, 2, 10, 4)
available_p <- c(28, 18, 32, 9, 5, 14, 22)
exchangeable_k <- c(190, 110, 210, 160, 70, 180, 155)
ec <- c(0.8, 1.4, 5.8, 0.3, 2.2, 0.6, 0.7)
sar <- c(2, 4, 12, 1, 8, 2, 2)
erosion_risk <- c(0.22, 0.46, 0.30, 0.12, 0.82, 0.08, 0.25)
compaction_risk <- c(0.18, 0.35, 0.25, 0.10, 0.65, 0.20, 0.30)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

ph_stress <- ifelse(pH < 6, clamp01((6 - pH) / 2),
                    ifelse(pH > 7.8, clamp01((pH - 7.8) / 2), 0))

nutrient_balance <- clamp01(
  0.40 * clamp01((nitrate + ammonium) / 60) +
  0.30 * clamp01(available_p / 40) +
  0.30 * clamp01(exchangeable_k / 250)
)

organic_score <- clamp01(organic_matter / 6)
cec_score <- clamp01(cec / 25)
salinity_sodicity <- pmax(clamp01((ec - 2) / 6), clamp01((sar - 6) / 12))

soil_pressure <- clamp01(
  0.22 * (1 - nutrient_balance) +
  0.18 * salinity_sodicity +
  0.16 * ph_stress +
  0.16 * erosion_risk +
  0.12 * compaction_risk +
  0.10 * (1 - organic_score) +
  0.06 * (1 - cec_score)
)

data <- data.frame(
  site,
  land_use,
  soil_group,
  pH,
  organic_matter,
  cec,
  nitrate,
  ammonium,
  available_p,
  exchangeable_k,
  nutrient_balance,
  ph_stress,
  salinity_sodicity,
  erosion_risk,
  compaction_risk,
  soil_pressure
)

land_use_summary <- aggregate(
  cbind(nutrient_balance, organic_matter, cec, soil_pressure) ~ land_use,
  data = data,
  FUN = mean
)

soil_group_summary <- aggregate(
  cbind(nutrient_balance, soil_pressure) ~ soil_group,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_soil_indicators.csv", row.names = FALSE)
write.csv(land_use_summary, "../outputs/tables/r_full_stack_soil_land_use_summary.csv", row.names = FALSE)
write.csv(soil_group_summary, "../outputs/tables/r_full_stack_soil_group_summary.csv", row.names = FALSE)

print(land_use_summary)
print(soil_group_summary)
