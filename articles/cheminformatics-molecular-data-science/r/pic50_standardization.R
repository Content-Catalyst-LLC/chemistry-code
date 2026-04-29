# pIC50 standardization scaffold.
# Synthetic educational examples only.

assays <- read.csv(file.path("data", "assays.csv"))

assays$value_M <- ifelse(tolower(assays$unit) == "nm", assays$value * 1e-9, NA)
assays$p_activity <- -log10(assays$value_M)

print(assays)
