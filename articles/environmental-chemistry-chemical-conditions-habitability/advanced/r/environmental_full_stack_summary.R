# Environmental Chemistry and the Chemical Conditions of Habitability
# R compartment and analyte-class summary.
# Synthetic educational code only.

site <- c("SurfaceWater-A", "Groundwater-B", "Soil-C", "Sediment-D", "Stormwater-F", "Wetland-G", "Groundwater-I")
compartment <- c("surface_water", "groundwater", "soil", "sediment", "stormwater", "wetland_water", "groundwater")
analyte_class <- c("nutrient", "metalloid", "metal", "pah", "metal", "nutrient", "chlorinated_solvent")
benchmark_ratio <- c(0.82, 1.35, 1.05, 1.90, 1.33, 2.10, 1.70)
mobility_factor <- c(0.70, 0.80, 0.25, 0.02, 0.45, 0.55, 0.83)
persistence_factor <- c(0.25, 0.999, 0.999, 0.71, 0.47, 0.33, 0.80)
exposure_weight <- c(0.70, 0.95, 0.85, 0.55, 0.72, 0.62, 0.93)
receptor_sensitivity <- c(0.75, 0.90, 0.88, 0.82, 0.78, 0.80, 0.91)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

pressure_index <- clamp01(
  0.30 * clamp01(log1p(benchmark_ratio) / log(5)) +
  0.18 * mobility_factor +
  0.18 * persistence_factor +
  0.18 * exposure_weight +
  0.16 * receptor_sensitivity
)

data <- data.frame(
  site,
  compartment,
  analyte_class,
  benchmark_ratio,
  mobility_factor,
  persistence_factor,
  exposure_weight,
  receptor_sensitivity,
  pressure_index
)

compartment_summary <- aggregate(
  cbind(benchmark_ratio, mobility_factor, persistence_factor, pressure_index) ~ compartment,
  data = data,
  FUN = mean
)

class_summary <- aggregate(
  cbind(benchmark_ratio, pressure_index) ~ analyte_class,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_environmental_indicators.csv", row.names = FALSE)
write.csv(compartment_summary, "../outputs/tables/r_full_stack_environmental_compartment_summary.csv", row.names = FALSE)
write.csv(class_summary, "../outputs/tables/r_full_stack_environmental_analyte_class_summary.csv", row.names = FALSE)

print(compartment_summary)
print(class_summary)
