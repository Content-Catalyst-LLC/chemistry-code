# Circular Chemistry, Waste, and Material Futures
# R circularity summary by material class.
# Synthetic educational code only.

material_stream <- c("PET_bottles_clear", "Multilayer_film", "Aluminum_scrap", "Lithium_ion_batteries", "Solvent_wash_stream", "Textile_polycotton", "E_waste_circuit_boards", "Compostable_packaging")
material_class <- c("polymer", "polymer", "metal", "battery", "solvent", "textile", "electronics", "biopolymer")
input_waste_kg <- c(1000, 1000, 800, 500, 1500, 900, 700, 1000)
recovered_kg <- c(760, 420, 720, 310, 1260, 430, 260, 540)
quality_factor <- c(0.82, 0.58, 0.94, 0.78, 0.88, 0.60, 0.82, 0.52)
substitution_factor <- c(0.72, 0.45, 0.90, 0.72, 0.86, 0.50, 0.88, 0.38)
hazard_score <- c(0.18, 0.34, 0.16, 0.48, 0.32, 0.30, 0.52, 0.20)
exposure_relevance <- c(0.22, 0.35, 0.18, 0.55, 0.46, 0.40, 0.62, 0.28)
contamination_score <- c(0.18, 0.62, 0.12, 0.40, 0.20, 0.55, 0.70, 0.32)
traceability_score <- c(0.78, 0.35, 0.82, 0.70, 0.75, 0.46, 0.58, 0.62)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

recovery_yield <- recovered_kg / input_waste_kg
circular_retention <- recovery_yield * quality_factor * substitution_factor
safe_circularity_score <- clamp01(
  0.35 * (1 - hazard_score) +
  0.30 * (1 - exposure_relevance) +
  0.25 * (1 - contamination_score) +
  0.10 * traceability_score
)

circular_chemistry_score <- clamp01(
  0.24 * recovery_yield +
  0.26 * circular_retention +
  0.24 * safe_circularity_score +
  0.16 * traceability_score +
  0.10 * substitution_factor
)

data <- data.frame(
  material_stream,
  material_class,
  input_waste_kg,
  recovered_kg,
  recovery_yield,
  circular_retention,
  safe_circularity_score,
  traceability_score,
  circular_chemistry_score
)

class_summary <- aggregate(
  cbind(recovery_yield, circular_retention, safe_circularity_score, circular_chemistry_score) ~ material_class,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_circular_chemistry_indicators.csv", row.names = FALSE)
write.csv(class_summary, "../outputs/tables/r_full_stack_circular_material_class_summary.csv", row.names = FALSE)

print(class_summary)
