# VSEPR-style molecular geometry metadata summary.

vsepr <- read.csv(file.path("data", "vsepr_examples.csv"))

summary <- aggregate(
  molecule ~ molecular_geometry,
  data = vsepr,
  FUN = length
)

names(summary)[2] <- "count"

print(vsepr)
print(summary)
