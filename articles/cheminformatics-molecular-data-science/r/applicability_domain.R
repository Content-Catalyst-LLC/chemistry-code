# Applicability-domain distance scaffold.
# Synthetic educational descriptor data only.

descriptors <- read.csv(file.path("data", "descriptors.csv"))
splits <- read.csv(file.path("data", "scaffold_splits.csv"))
queries <- read.csv(file.path("data", "query_descriptors.csv"))

train <- merge(descriptors, splits[, c("molecule_id", "split")], by = "molecule_id")
train <- train[train$split == "train", ]

feature_cols <- c(
  "heavy_atoms",
  "hetero_atoms",
  "rings",
  "h_bond_donors",
  "h_bond_acceptors",
  "rotatable_bonds"
)

distance_to_train <- function(query_row) {
  query_vector <- as.numeric(query_row[feature_cols])
  train_matrix <- as.matrix(train[, feature_cols])
  distances <- sqrt(rowSums((t(t(train_matrix) - query_vector))^2))
  min(distances)
}

queries$nearest_training_distance <- apply(queries, 1, distance_to_train)

print(queries)
