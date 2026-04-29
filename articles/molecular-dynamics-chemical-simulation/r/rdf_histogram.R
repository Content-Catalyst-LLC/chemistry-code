# RDF-like histogram scaffold.
# Synthetic educational distances only.

distances <- read.csv(file.path("data", "rdf_distances.csv"))

breaks <- seq(0.5, 3.5, by = 0.5)
counts <- hist(distances$distance, breaks = breaks, plot = FALSE)

rdf_table <- data.frame(
  r_midpoint = counts$mids,
  count = counts$counts
)

print(rdf_table)
