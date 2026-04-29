# Chromatographic resolution scaffold.
# Synthetic educational examples only.

peaks <- read.csv(file.path("data", "chromatography_peaks.csv"))

peaks$resolution <- 2 * (peaks$tR_2_min - peaks$tR_1_min) /
  (peaks$w1_min + peaks$w2_min)

peaks$baseline_separation_hint <- as.integer(peaks$resolution >= 1.5)

print(peaks)
