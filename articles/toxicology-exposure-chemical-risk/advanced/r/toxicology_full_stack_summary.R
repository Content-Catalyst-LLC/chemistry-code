# Toxicology, Exposure, and Chemical Risk
# R target-system and mixture hazard summaries.
# Synthetic educational code only.

chemical <- c("arsenic", "lead", "mercury", "benzene", "ozone", "formaldehyde", "PFOS")
target_system <- c("cancer_and_skin", "neurodevelopment", "neurodevelopment", "bone_marrow", "respiratory", "respiratory", "immune_endocrine")
mixture_group <- c("metals_metalloids", "metals_metalloids", "metals_metalloids", "volatile_organics", "air_pollutants", "irritants", "persistent_organics")
hazard_quotient <- c(0.030, 0.120, 0.420, 0.080, 0.190, 0.085, 0.900)
vulnerability_factor <- c(1.20, 1.80, 1.50, 1.10, 1.25, 1.05, 1.35)

data <- data.frame(
  chemical,
  target_system,
  mixture_group,
  hazard_quotient,
  vulnerability_factor
)

data$vulnerability_adjusted_hazard <- data$hazard_quotient * data$vulnerability_factor

target_summary <- aggregate(
  cbind(hazard_quotient, vulnerability_adjusted_hazard) ~ target_system,
  data = data,
  FUN = sum
)

mixture_summary <- aggregate(
  cbind(hazard_quotient, vulnerability_adjusted_hazard) ~ mixture_group,
  data = data,
  FUN = sum
)

dir.create("../outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(data, "../outputs/tables/r_full_stack_toxicology_indicators.csv", row.names = FALSE)
write.csv(target_summary, "../outputs/tables/r_full_stack_target_system_summary.csv", row.names = FALSE)
write.csv(mixture_summary, "../outputs/tables/r_full_stack_mixture_group_summary.csv", row.names = FALSE)

print(target_summary)
print(mixture_summary)
