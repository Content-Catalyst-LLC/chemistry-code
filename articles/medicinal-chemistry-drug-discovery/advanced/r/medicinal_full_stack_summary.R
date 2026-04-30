# Medicinal Chemistry and Drug Discovery
# R project-level discovery analytics.
# Synthetic educational code only.

compound_id <- c("MEDADV001", "MEDADV002", "MEDADV003", "MEDADV006", "MEDADV008", "MEDADV010")
project <- c("Kinase-A", "Kinase-A", "GPCR-B", "Enzyme-E", "Kinase-A", "GPCR-B")
ic50_nM <- c(18, 42, 7, 32, 4, 22)
off_target_ic50_nM <- c(2100, 980, 320, 5200, 4800, 650)
clogP <- c(3.2, 4.1, 2.8, 1.9, 4.6, 3.1)
hERG_ic50_uM <- c(18, 9, 4, 42, 25, 6)
solubility_uM <- c(45, 28, 65, 160, 34, 75)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

pIC50 <- -log10(ic50_nM * 1e-9)
selectivity_window <- off_target_ic50_nM / ic50_nM
LLE <- pIC50 - clogP
hERG_risk <- clamp01((10 - hERG_ic50_uM) / 10)
solubility_score <- clamp01(log10(pmax(solubility_uM, 0.001)) / 2.3)

MPO <- clamp01(
  0.30 * clamp01((pIC50 - 5) / 3) +
  0.22 * clamp01(log10(pmax(selectivity_window, 1)) / 3) +
  0.20 * clamp01((LLE - 2) / 5) +
  0.16 * solubility_score +
  0.12 * (1 - hERG_risk)
)

data <- data.frame(
  compound_id,
  project,
  pIC50,
  selectivity_window,
  LLE,
  hERG_risk,
  solubility_score,
  MPO
)

summary <- aggregate(
  cbind(pIC50, selectivity_window, LLE, hERG_risk, MPO) ~ project,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_medicinal_indicators.csv", row.names = FALSE)
write.csv(summary, "../outputs/tables/r_full_stack_medicinal_project_summary.csv", row.names = FALSE)

print(summary)
