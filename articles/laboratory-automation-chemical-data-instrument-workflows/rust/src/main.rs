use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("run_manifest.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read laboratory automation run manifest.");

    let mut instruments = BTreeSet::new();
    let mut methods = BTreeSet::new();
    let mut statuses = BTreeSet::new();
    let mut row_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 11 {
            eprintln!("Malformed run manifest row {}: expected 11 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        instruments.insert(fields[3].to_string());
        methods.insert(fields[4].to_string());
        statuses.insert(fields[9].to_string());
        row_count += 1;
    }

    println!("Laboratory automation manifest validation");
    println!("Run rows: {}", row_count);
    println!("Instruments: {:?}", instruments);
    println!("Methods: {:?}", methods);
    println!("QC statuses: {:?}", statuses);
    println!("Responsible-use note: synthetic educational data only.");
}
