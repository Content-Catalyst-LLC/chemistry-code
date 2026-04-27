# Simplified historical-to-modern nomenclature mapping.

nomenclature <- read.csv(file.path("data", "nomenclature_mapping.csv"), stringsAsFactors = FALSE)

nomenclature <- nomenclature[order(nomenclature$conceptual_shift, nomenclature$older_name), ]

print(nomenclature)
