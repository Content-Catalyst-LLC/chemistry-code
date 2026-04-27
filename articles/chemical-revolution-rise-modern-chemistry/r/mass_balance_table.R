# Conservation of mass table using synthetic examples.

reactions <- read.csv(file.path("data", "mass_conservation_examples.csv"))

reactions$mass_difference_g <- reactions$product_mass_g - reactions$reactant_mass_g
reactions$conserved_exactly <- abs(reactions$mass_difference_g) < 1e-9

print(reactions)
