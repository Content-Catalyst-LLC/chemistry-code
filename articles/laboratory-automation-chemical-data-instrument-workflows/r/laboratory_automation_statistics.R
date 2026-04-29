#!/usr/bin/env Rscript

# Synthetic laboratory automation statistics workflow.
# Educational data only.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grep(file_arg, args)])

if (length(script_path) == 0) {
  script_path <- "r/laboratory_automation_statistics.R"
}

base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
data_dir <- file.path(base_dir, "data")
table_dir <- file.path(base_dir, "outputs", "tables")
report_dir <- file.path(base_dir, "outputs", "reports")

dir.create(table_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(report_dir, recursive = TRUE, showWarnings = FALSE)

runs <- read.csv(file.path(data_dir, "run_manifest.csv"), stringsAsFactors = FALSE)
qc <- read.csv(file.path(data_dir, "qc_results.csv"), stringsAsFactors = FALSE)
methods <- read.csv(file.path(data_dir, "instrument_methods.csv"), stringsAsFactors = FALSE)

runs$scheduled_time <- as.POSIXct(runs$scheduled_time, format = "%Y-%m-%d %H:%M", tz = "UTC")
runs$completed_time <- as.POSIXct(runs$completed_time, format = "%Y-%m-%d %H:%M", tz = "UTC")
runs$turnaround_min <- as.numeric(difftime(runs$completed_time, runs$scheduled_time, units = "mins"))

instrument_summary <- aggregate(
  turnaround_min ~ instrument_id,
  data = runs,
  FUN = function(x) c(mean = mean(x, na.rm = TRUE), max = max(x, na.rm = TRUE), n = sum(!is.na(x)))
)

instrument_summary_clean <- data.frame(
  instrument_id = instrument_summary$instrument_id,
  mean_turnaround_min = instrument_summary$turnaround_min[, "mean"],
  max_turnaround_min = instrument_summary$turnaround_min[, "max"],
  completed_run_count = instrument_summary$turnaround_min[, "n"]
)

qc_numeric <- qc[qc$metric_name == "response_ratio", ]
drift_summary <- data.frame(
  qc_count = nrow(qc_numeric),
  mean_qc_response = mean(qc_numeric$metric_value),
  min_qc_response = min(qc_numeric$metric_value),
  max_qc_response = max(qc_numeric$metric_value),
  warning_count = sum(qc$qc_status == "warning"),
  failed_count = sum(qc$qc_status == "failed")
)

status_summary <- as.data.frame(table(runs$qc_status))
names(status_summary) <- c("qc_status", "run_count")

write.csv(instrument_summary_clean, file.path(table_dir, "r_instrument_turnaround_summary.csv"), row.names = FALSE)
write.csv(drift_summary, file.path(table_dir, "r_qc_response_summary.csv"), row.names = FALSE)
write.csv(status_summary, file.path(table_dir, "r_run_status_summary.csv"), row.names = FALSE)

sink(file.path(report_dir, "r_laboratory_automation_statistics_report.txt"))
cat("Synthetic Laboratory Automation Statistics Report\n")
cat("================================================\n\n")
cat("Instrument turnaround summary:\n")
print(instrument_summary_clean)
cat("\nQC response summary:\n")
print(drift_summary)
cat("\nRun status summary:\n")
print(status_summary)
cat("\nMethod records:\n")
print(methods)
cat("\nResponsible-use note: synthetic educational data only.\n")
sink()

message("R laboratory automation statistics workflow complete.")
