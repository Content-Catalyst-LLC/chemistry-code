# Food Chemistry and the Molecular Basis of Nutrition
# R food-group summary example.
# Synthetic educational code only.

food <- c("lentils_cooked", "oats_cooked", "walnuts", "orange_segments", "spinach_cooked")
food_group <- c("legume", "whole_grain", "nut_seed", "fruit", "leafy_green")
energy_kcal <- c(230, 180, 330, 80, 45)
protein_g <- c(18, 10, 15, 1.5, 5)
fiber_g <- c(15, 8, 7, 4, 4)
potassium_mg <- c(730, 180, 320, 240, 840)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

nutrient_density <- function(protein_g, fiber_g, potassium_mg, energy_kcal) {
  beneficial <- 0.40 * clamp01(protein_g / 25) +
    0.35 * clamp01(fiber_g / 12) +
    0.25 * clamp01(potassium_mg / 800)

  energy_factor <- pmax(energy_kcal / 100, 0.5)
  beneficial / energy_factor
}

data <- data.frame(
  food,
  food_group,
  energy_kcal,
  protein_g,
  fiber_g,
  potassium_mg
)

data$nutrient_density <- nutrient_density(
  data$protein_g,
  data$fiber_g,
  data$potassium_mg,
  data$energy_kcal
)

summary <- aggregate(
  nutrient_density ~ food_group,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_food_chemistry_indicators.csv", row.names = FALSE)
write.csv(summary, "../outputs/tables/r_full_stack_food_group_summary.csv", row.names = FALSE)

print(summary)
