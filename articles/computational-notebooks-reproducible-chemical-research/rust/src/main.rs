use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("synthetic_chemical_notebook_runs.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read synthetic chemical notebook data.");

    let mut notebooks = BTreeSet::new();
    let mut environments = BTreeSet::new();
    let mut instruments = BTreeSet::new();
    let mut row_count = 0usize;

    for (i, line) in content.lines().enumerate() {
        if i == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 12 {
            eprintln!("Malformed row {}: expected 12 fields, found {}", i + 1, fields.len());
            std::process::exit(1);
        }

        notebooks.insert(fields[1].to_string());
        instruments.insert(fields[4].to_string());
        environments.insert(fields[5].to_string());
        row_count += 1;
    }

    println!("Chemical notebook manifest validation");
    println!("Rows: {}", row_count);
    println!("Notebook IDs: {:?}", notebooks);
    println!("Instrument IDs: {:?}", instruments);
    println!("Environment IDs: {:?}", environments);
    println!("Responsible-use note: synthetic educational data only.");
}
