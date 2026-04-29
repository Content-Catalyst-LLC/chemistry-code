# Sequence composition scaffold.
# Synthetic educational sequences only.

sequences <- read.csv(file.path("data", "sequences.csv"))

for (i in seq_len(nrow(sequences))) {
  sequence_id <- sequences$sequence_id[i]
  sequence <- strsplit(sequences$sequence[i], "")[[1]]
  counts <- table(sequence)
  composition <- data.frame(
    sequence_id = sequence_id,
    symbol = names(counts),
    count = as.integer(counts),
    fraction = as.numeric(counts) / length(sequence)
  )
  print(composition)
}
