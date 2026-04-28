# Hess's law using simplified formation enthalpy data.

formation <- read.csv(file.path("data", "formation_enthalpy_examples.csv"))

formation$contribution_kj_mol <- formation$coefficient *
  formation$delta_h_f_kj_mol

summary <- aggregate(
  contribution_kj_mol ~ reaction_id,
  data = formation,
  FUN = sum
)

names(summary)[2] <- "delta_h_reaction_kj_mol"

print(formation)
print(summary)
