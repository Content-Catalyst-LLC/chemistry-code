# Perturbation-vector scaffold.
# Synthetic educational examples only.

features <- read.csv(file.path("data", "perturbation_features.csv"))

features$delta <- features$treated - features$control
features$absolute_delta <- abs(features$delta)

print(features[order(-features$absolute_delta), ])
