# Replicate summary scaffold.
# Synthetic educational data only.

measurements <- read.csv(file.path("data", "replicate_measurements.csv"))

mean_table <- aggregate(measurement_mM ~ sample_id + method_id, data = measurements, mean)
sd_table <- aggregate(measurement_mM ~ sample_id + method_id, data = measurements, sd)
n_table <- aggregate(measurement_mM ~ sample_id + method_id, data = measurements, length)

summary_table <- merge(mean_table, sd_table, by = c("sample_id", "method_id"), suffixes = c("_mean", "_sd"))
summary_table <- merge(summary_table, n_table, by = c("sample_id", "method_id"))
names(summary_table)[names(summary_table) == "measurement_mM"] <- "n"

summary_table$se_mM <- summary_table$measurement_mM_sd / sqrt(summary_table$n)

print(summary_table)
