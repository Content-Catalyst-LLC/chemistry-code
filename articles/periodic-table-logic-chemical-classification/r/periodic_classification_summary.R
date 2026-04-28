# Periodic classification summary using simplified educational data.

elements <- read.csv(file.path("data", "elements_classification.csv"))

by_block <- aggregate(symbol ~ block, data = elements, FUN = length)
names(by_block)[2] <- "count"

by_category <- aggregate(symbol ~ category, data = elements, FUN = length)
names(by_category)[2] <- "count"

by_family <- aggregate(symbol ~ family, data = elements, FUN = length)
names(by_family)[2] <- "count"

print(by_block)
print(by_category[order(-by_category$count, by_category$category), ])
print(by_family[order(-by_family$count, by_family$family), ])
