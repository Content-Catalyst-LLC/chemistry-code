# Henderson-Hasselbalch buffer pH calculation.
# Synthetic educational data only.

buffers <- read.csv(file.path("data", "buffer_cases.csv"))

buffers$base_to_acid_ratio <- buffers$conjugate_base_mol_l / buffers$weak_acid_mol_l
buffers$pH <- buffers$pKa + log10(buffers$base_to_acid_ratio)
buffers$total_buffer_mol_l <- buffers$conjugate_base_mol_l + buffers$weak_acid_mol_l

print(buffers)
