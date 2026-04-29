# Probe quality scaffold.
# Synthetic educational examples only.

probes <- read.csv(file.path("data", "probe_quality_cases.csv"))

probes$selectivity_ratio <- probes$off_target_potency_nM / probes$target_potency_nM

probes$quality_score <- (
  pmin(probes$selectivity_ratio, 100) / 100 +
    probes$cellular_target_engagement +
    0.25 * probes$inactive_control_available +
    0.10 * probes$solubility_flag +
    0.10 * probes$viability_flag
)

print(probes)
