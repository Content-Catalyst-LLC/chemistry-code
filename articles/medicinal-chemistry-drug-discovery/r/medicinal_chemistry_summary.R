# Medicinal chemistry synthetic project summary.
# Educational only.

data <- read.csv("../data/medicinal_chemistry_synthetic.csv")

data$pIC50 <- -log10(data$ic50_nM * 1e-9)
data$selectivity_window <- data$off_target_ic50_nM / data$ic50_nM
data$LLE <- data$pIC50 - data$clogP

summary <- aggregate(
  cbind(pIC50, selectivity_window, LLE) ~ project,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_medicinal_chemistry_indicators.csv", row.names = FALSE)
write.csv(summary, "../outputs/tables/r_project_summary.csv", row.names = FALSE)

print(summary)
