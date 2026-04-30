# Water Chemistry and Environmental Monitoring
# R water-body and analyte summary.
# Synthetic educational code only.

site <- c("River-A", "Lake-B", "Well-C", "Storm-D", "Estuary-E", "Wetland-F", "Reservoir-G")
water_body <- c("river", "lake", "aquifer", "urban_runoff", "estuary", "wetland", "reservoir")
analyte <- c("nitrate_as_N", "dissolved_oxygen", "arsenic", "lead", "copper", "phosphate_as_P", "nitrate_as_N")
benchmark_ratio <- c(0.78, 0.92, 1.20, 1.20, 1.08, 0.90, 0.32)
oxygen_stress <- c(0.13, 0.54, 0.75, 0.30, 0.25, 0.42, 0.20)
nutrient_index <- c(0.84, 0.39, 0.06, 1.00, 0.87, 0.53, 0.29)
metal_index <- c(0.25, 0.18, 0.44, 0.88, 0.55, 0.20, 0.14)
turbidity_pressure <- c(0.12, 0.18, 0.01, 0.75, 0.22, 0.34, 0.09)
qc_score <- c(0.93, 0.88, 0.86, 0.80, 0.84, 0.90, 0.94)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

pressure_index <- clamp01(
  0.22 * clamp01(log1p(benchmark_ratio) / log(4)) +
  0.18 * oxygen_stress +
  0.20 * nutrient_index +
  0.20 * metal_index +
  0.12 * turbidity_pressure +
  0.08 * (1 - qc_score)
)

data <- data.frame(
  site,
  water_body,
  analyte,
  benchmark_ratio,
  oxygen_stress,
  nutrient_index,
  metal_index,
  turbidity_pressure,
  qc_score,
  pressure_index
)

water_body_summary <- aggregate(
  cbind(benchmark_ratio, oxygen_stress, nutrient_index, metal_index, pressure_index) ~ water_body,
  data = data,
  FUN = mean
)

analyte_summary <- aggregate(
  cbind(benchmark_ratio, pressure_index) ~ analyte,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_water_indicators.csv", row.names = FALSE)
write.csv(water_body_summary, "../outputs/tables/r_full_stack_water_body_summary.csv", row.names = FALSE)
write.csv(analyte_summary, "../outputs/tables/r_full_stack_water_analyte_summary.csv", row.names = FALSE)

print(water_body_summary)
print(analyte_summary)
