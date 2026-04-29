# Generate a markdown report for R chemistry statistics workflow.
# Synthetic educational data only.

suppressPackageStartupMessages({
  library(readr)
})

article_dir <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
report_path <- file.path(article_dir, "outputs", "reports", "r_chemistry_report.md")
dir.create(dirname(report_path), recursive = TRUE, showWarnings = FALSE)

required_files <- c(
  file.path(article_dir, "outputs", "tables", "replicate_summary.csv"),
  file.path(article_dir, "outputs", "tables", "calibration_model.csv"),
  file.path(article_dir, "outputs", "tables", "unknown_concentrations.csv"),
  file.path(article_dir, "outputs", "tables", "first_order_kinetics.csv"),
  file.path(article_dir, "outputs", "tables", "arrhenius_transform.csv"),
  file.path(article_dir, "outputs", "tables", "anova_summary.csv"),
  file.path(article_dir, "outputs", "tables", "qc_summary.csv")
)

scripts <- c(
  "01_replicate_summary.R",
  "02_calibration_curve.R",
  "03_kinetics_arrhenius.R",
  "04_anova_qc.R"
)

for (script in scripts) {
  system2("Rscript", file.path(article_dir, "r", script))
}

read_or_empty <- function(path) {
  if (file.exists(path)) {
    paste(capture.output(print(read_csv(path, show_col_types = FALSE))), collapse = "\n")
  } else {
    "File not available."
  }
}

report <- c(
  "# R for Chemistry, Statistics, and Experimental Analysis",
  "",
  "This report was generated from simplified educational chemical statistics data.",
  "",
  "## Replicate Summary",
  "",
  "```",
  read_or_empty(required_files[1]),
  "```",
  "",
  "## Calibration Model",
  "",
  "```",
  read_or_empty(required_files[2]),
  "```",
  "",
  "## Unknown Concentrations",
  "",
  "```",
  read_or_empty(required_files[3]),
  "```",
  "",
  "## First-Order Kinetics",
  "",
  "```",
  read_or_empty(required_files[4]),
  "```",
  "",
  "## Arrhenius Transform",
  "",
  "```",
  read_or_empty(required_files[5]),
  "```",
  "",
  "## ANOVA Summary",
  "",
  "```",
  read_or_empty(required_files[6]),
  "```",
  "",
  "## Quality-Control Summary",
  "",
  "```",
  read_or_empty(required_files[7]),
  "```",
  "",
  "## Interpretation Warning",
  "",
  "These examples are educational scaffolds. Real chemical analysis requires validated analytical methods, calibrated instruments, documented sample preparation, quality-control standards, appropriate statistical assumptions, uncertainty budgets, and expert chemical interpretation.",
  ""
)

writeLines(report, report_path)
cat(paste(report, collapse = "\n"))
cat("\nSaved:", report_path, "\n")
