# Dilution planning using C1V1 = C2V2.

dilutions <- read.csv(file.path("data", "dilution_plan.csv"))

dilutions$stock_volume_ml <- with(
  dilutions,
  (target_concentration_mol_l * final_volume_ml) / stock_concentration_mol_l
)

dilutions$diluent_volume_ml <- dilutions$final_volume_ml - dilutions$stock_volume_ml

print(round(dilutions, 6))
