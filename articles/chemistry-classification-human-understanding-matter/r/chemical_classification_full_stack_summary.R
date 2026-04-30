# Chemistry, Classification, and the Human Understanding of Matter
# R chemical class summary.
# Synthetic educational code only.

sample_name <- c("ethyl_acetate_reference", "seawater_sample", "sodium_chloride_crystal", "polyethylene_film", "iron_oxide_powder", "cobalt_complex", "soil_extract", "silica_glass")
assigned_class <- c("organic_molecular_substance", "mixture_or_solution", "ionic_or_salt_crystal", "polymer_material", "extended_solid_or_network_material", "coordination_compound", "heterogeneous_mixture", "extended_solid_or_network_material")
phase <- c("liquid", "aqueous_solution", "crystalline_solid", "solid", "crystalline_solid", "crystalline_solid", "heterogeneous_mixture", "amorphous_solid")
spectral_match_score <- c(0.92, 0.70, 0.88, 0.80, 0.82, 0.76, 0.48, 0.84)
elemental_match_score <- c(0.88, 0.82, 0.93, 0.68, 0.90, 0.84, 0.72, 0.86)
thermal_signature_score <- c(0.74, 0.40, 0.70, 0.86, 0.78, 0.66, 0.55, 0.82)
classification_confidence <- c(0.86, 0.74, 0.91, 0.82, 0.84, 0.80, 0.60, 0.83)
hazard_indicator_score <- c(0.22, 0.35, 0.18, 0.20, 0.30, 0.45, 0.62, 0.12)
qc_score <- c(0.94, 0.90, 0.96, 0.92, 0.91, 0.89, 0.82, 0.93)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

evidence_score <- clamp01(
  0.35 * spectral_match_score +
  0.30 * elemental_match_score +
  0.20 * thermal_signature_score +
  0.15 * qc_score
)

classification_reliability <- clamp01(
  0.55 * evidence_score +
  0.30 * classification_confidence +
  0.15 * qc_score
)

data <- data.frame(
  sample_name,
  assigned_class,
  phase,
  evidence_score,
  classification_reliability,
  hazard_indicator_score,
  qc_score
)

class_summary <- aggregate(
  cbind(evidence_score, classification_reliability, hazard_indicator_score, qc_score) ~ assigned_class,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_chemical_classification_indicators.csv", row.names = FALSE)
write.csv(class_summary, "../outputs/tables/r_full_stack_chemical_class_summary.csv", row.names = FALSE)

print(class_summary)
