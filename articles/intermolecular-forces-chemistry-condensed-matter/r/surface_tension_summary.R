# Surface tension summary using simplified educational data.

surface <- read.csv(file.path("data", "surface_tension_sample.csv"))

print(surface)

summary <- aggregate(
  surface_tension_mN_m ~ dominant_interaction,
  data = surface,
  FUN = mean
)

names(summary)[2] <- "mean_surface_tension_mN_m"

print(summary[order(-summary$mean_surface_tension_mN_m), ])
