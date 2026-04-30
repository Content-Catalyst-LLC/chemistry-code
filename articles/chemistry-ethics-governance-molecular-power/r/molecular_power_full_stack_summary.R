# Chemistry, Ethics, and the Governance of Molecular Power
# R governance summary by chemical domain.
# Synthetic educational code only.

domain <- c("medicine", "agriculture", "industrial_material", "consumer_product", "water_treatment", "dual_use", "energy_storage", "circular_material")
context <- c("essential_therapeutic", "high_volume_pesticide", "persistent_additive", "indoor_exposure_chemical", "disinfection_chemical", "restricted_toxic_precursor", "battery_material_supply_chain", "recycled_additive_stream")
benefit <- c(0.95, 0.72, 0.58, 0.48, 0.90, 0.22, 0.82, 0.62)
hazard <- c(0.35, 0.68, 0.72, 0.52, 0.58, 0.92, 0.46, 0.60)
exposure <- c(0.42, 0.76, 0.64, 0.78, 0.48, 0.35, 0.52, 0.58)
vulnerability <- c(0.55, 0.84, 0.70, 0.76, 0.62, 0.88, 0.70, 0.68)
inequality <- c(0.22, 0.58, 0.65, 0.60, 0.35, 0.52, 0.74, 0.64)
worker <- c(0.30, 0.72, 0.42, 0.38, 0.55, 0.68, 0.66, 0.50)
governance <- c(0.82, 0.55, 0.42, 0.38, 0.76, 0.88, 0.50, 0.44)
transparency <- c(0.78, 0.45, 0.32, 0.36, 0.70, 0.22, 0.50, 0.42)
dual_use <- c(0.05, 0.12, 0.08, 0.04, 0.10, 0.95, 0.06, 0.05)

clamp01 <- function(x) {
  pmax(0, pmin(1, x))
}

risk <- clamp01(hazard * exposure * vulnerability)
justice_weighted_risk <- clamp01(risk * (1 + 0.50 * inequality + 0.35 * worker))
governance_gap <- clamp01(justice_weighted_risk * (1 - governance))
responsible_score <- clamp01(
  0.32 * benefit +
  0.24 * governance +
  0.18 * transparency -
  0.18 * justice_weighted_risk -
  0.08 * dual_use
)

data <- data.frame(
  domain,
  context,
  benefit,
  risk,
  justice_weighted_risk,
  governance_gap,
  governance,
  transparency,
  dual_use,
  responsible_score
)

domain_summary <- aggregate(
  cbind(benefit, justice_weighted_risk, governance_gap, governance, transparency, responsible_score) ~ domain,
  data = data,
  FUN = mean
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_molecular_power_indicators.csv", row.names = FALSE)
write.csv(domain_summary, "../outputs/tables/r_full_stack_molecular_power_domain_summary.csv", row.names = FALSE)

print(domain_summary)
