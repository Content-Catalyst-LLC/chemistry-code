# Precision and spike recovery scaffold.
# Synthetic educational examples only.

measurements <- read.csv(file.path("data", "replicate_measurements.csv"))
spikes <- read.csv(file.path("data", "spike_recovery.csv"))

precision <- aggregate(
  measured_mg_L ~ sample_id,
  data = measurements,
  FUN = function(x) c(mean = mean(x), sd = sd(x), rsd_percent = 100 * sd(x) / mean(x))
)

spikes$recovery_percent <- 100 * (
  spikes$spiked_mg_L - spikes$unspiked_mg_L
) / spikes$spike_added_mg_L

print(precision)
print(spikes)
