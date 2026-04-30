# Green Chemistry, Responsibility, and Sustainable Transformation
# R route and chemistry-class summary.
# Synthetic educational code only.

route <- c("Route_A_Stoichiometric", "Route_B_Catalytic", "Route_C_Biocatalytic", "Route_D_Solvent_Intensive", "Route_E_Renewable_Feedstock", "Route_F_Flow_Chemistry", "Route_G_Persistent_Product", "Route_H_Circular_Material")
chemistry_class <- c("small_molecule_intermediate", "small_molecule_intermediate", "small_molecule_intermediate", "polymer_precursor", "polymer_precursor", "specialty_chemical", "consumer_additive", "consumer_material")
atom_economy <- c(180/260, 180/225, 180/215, 250/340, 250/310, 320/390, 410/520, 500/610)
e_factor <- c(28/2, 10/2.4, 6/1.8, 55/3, 14/2.5, 12/4, 30/5, 16/6)
pmi <- c(36/2, 18/2.4, 14/1.8, 72/3, 24/2.5, 28/4, 46/5, 38/6)
hazard_score <- c(0.55, 0.30, 0.22, 0.68, 0.34, 0.26, 0.42, 0.28)
solvent_hazard <- c(0.62, 0.35, 0.20, 0.74, 0.38, 0.28, 0.40, 0.30)
renewable <- c(0.20, 0.55, 0.70, 0.15, 0.82, 0.40, 0.30, 0.58)
circularity <- c(0.30, 0.62, 0.75, 0.20, 0.64, 0.70, 0.18, 0.86)
degradation <- c(0.25, 0.58, 0.72, 0.18, 0.55, 0.50, 0.08, 0.68)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

green_score <- clamp01(
  0.16 * clamp01(atom_economy) +
  0.16 * clamp01(1 - e_factor / 25) +
  0.14 * clamp01(1 - pmi / 30) +
  0.14 * clamp01(1 - hazard_score) +
  0.10 * clamp01(1 - solvent_hazard) +
  0.10 * renewable +
  0.10 * circularity +
  0.10 * degradation
)

data <- data.frame(
  route,
  chemistry_class,
  atom_economy,
  e_factor,
  pmi,
  hazard_score,
  solvent_hazard,
  renewable,
  circularity,
  degradation,
  green_score
)

class_summary <- aggregate(
  cbind(atom_economy, e_factor, pmi, hazard_score, green_score) ~ chemistry_class,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_green_chemistry_indicators.csv", row.names = FALSE)
write.csv(class_summary, "../outputs/tables/r_full_stack_green_chemistry_class_summary.csv", row.names = FALSE)

print(class_summary)
