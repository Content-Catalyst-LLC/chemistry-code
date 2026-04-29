-- SQL schema for synthetic laboratory automation records.
-- Educational only; adapt and validate before real laboratory or regulated use.

CREATE TABLE IF NOT EXISTS sample_queue (
    sample_id TEXT PRIMARY KEY,
    container_id TEXT NOT NULL,
    plate_position TEXT,
    received_time TEXT,
    priority TEXT,
    matrix TEXT,
    storage_condition TEXT
);

CREATE TABLE IF NOT EXISTS instrument_method (
    method_id TEXT PRIMARY KEY,
    method_name TEXT NOT NULL,
    instrument_type TEXT,
    version TEXT,
    validated_status TEXT,
    expected_runtime_min REAL,
    required_qc_type TEXT
);

CREATE TABLE IF NOT EXISTS instrument_run (
    run_id TEXT PRIMARY KEY,
    sample_id TEXT NOT NULL,
    sample_type TEXT,
    instrument_id TEXT NOT NULL,
    method_id TEXT NOT NULL,
    scheduled_time TEXT,
    completed_time TEXT,
    raw_file TEXT,
    processed_file TEXT,
    qc_status TEXT,
    exception_flag INTEGER,
    FOREIGN KEY (sample_id) REFERENCES sample_queue(sample_id),
    FOREIGN KEY (method_id) REFERENCES instrument_method(method_id)
);

CREATE TABLE IF NOT EXISTS qc_result (
    qc_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    instrument_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    lower_limit REAL,
    upper_limit REAL,
    qc_status TEXT,
    FOREIGN KEY (run_id) REFERENCES instrument_run(run_id)
);

CREATE TABLE IF NOT EXISTS data_file (
    file_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    file_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum_present INTEGER,
    format TEXT,
    created_time TEXT,
    FOREIGN KEY (run_id) REFERENCES instrument_run(run_id)
);

CREATE TABLE IF NOT EXISTS audit_event (
    event_id TEXT PRIMARY KEY,
    run_id TEXT,
    event_time TEXT,
    event_type TEXT,
    actor TEXT,
    details TEXT,
    FOREIGN KEY (run_id) REFERENCES instrument_run(run_id)
);
