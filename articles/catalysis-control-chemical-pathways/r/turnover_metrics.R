# Turnover number, turnover frequency, and catalytic activity.
# Synthetic educational data only.

experiments <- read.csv(file.path("data", "turnover_experiments.csv"))

experiments$TON <- experiments$product_mol / experiments$catalyst_mol
experiments$TOF_s_inv <- experiments$TON / experiments$time_s
experiments$catalytic_activity_mol_s <- experiments$product_mol / experiments$time_s

print(experiments)
