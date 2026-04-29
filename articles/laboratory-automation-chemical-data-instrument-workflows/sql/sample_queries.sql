-- Sample queries for synthetic laboratory automation workflows.

-- 1. Runs requiring manual review.
SELECT
    run_id,
    sample_id,
    instrument_id,
    method_id,
    qc_status,
    exception_flag,
    raw_file,
    processed_file
FROM instrument_run
WHERE qc_status <> 'pass'
   OR exception_flag = 1
   OR raw_file IS NULL
   OR processed_file IS NULL
ORDER BY scheduled_time;

-- 2. Instrument run counts and QC status summary.
SELECT
    instrument_id,
    qc_status,
    COUNT(*) AS run_count
FROM instrument_run
GROUP BY instrument_id, qc_status
ORDER BY instrument_id, qc_status;

-- 3. QC metrics outside limits.
SELECT
    qc_id,
    run_id,
    instrument_id,
    metric_name,
    metric_value,
    lower_limit,
    upper_limit,
    qc_status
FROM qc_result
WHERE metric_value < lower_limit
   OR metric_value > upper_limit
ORDER BY run_id;

-- 4. Data files missing checksums.
SELECT
    file_id,
    run_id,
    file_type,
    relative_path,
    format
FROM data_file
WHERE checksum_present = 0
ORDER BY run_id, file_type;

-- 5. Audit trail for a selected run.
SELECT
    event_time,
    event_type,
    actor,
    details
FROM audit_event
WHERE run_id = 'run_005'
ORDER BY event_time;
