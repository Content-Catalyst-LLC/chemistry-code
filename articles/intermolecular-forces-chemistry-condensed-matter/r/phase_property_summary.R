# Phase property summary using simplified educational data.

phase <- read.csv(file.path("data", "phase_properties_sample.csv"))

by_phase <- aggregate(
  substance ~ phase_at_room_conditions,
  data = phase,
  FUN = length
)

names(by_phase)[2] <- "count"

by_interaction <- aggregate(
  substance ~ dominant_interaction,
  data = phase,
  FUN = length
)

names(by_interaction)[2] <- "count"

print(phase)
print(by_phase)
print(by_interaction[order(-by_interaction$count), ])
