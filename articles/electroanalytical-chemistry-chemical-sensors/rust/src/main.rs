use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("electrochemical_metadata.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read electrochemical metadata.");

    let mut methods = BTreeSet::new();
    let mut electrodes = BTreeSet::new();
    let mut reference_electrodes = BTreeSet::new();
    let mut row_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 10 {
            eprintln!("Malformed metadata row {}: expected 10 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        methods.insert(fields[1].to_string());
        electrodes.insert(fields[3].to_string());
        reference_electrodes.insert(fields[5].to_string());
        row_count += 1;
    }

    println!("Electrochemical sensor manifest validation");
    println!("Metadata rows: {}", row_count);
    println!("Methods: {:?}", methods);
    println!("Electrodes: {:?}", electrodes);
    println!("Reference electrodes: {:?}", reference_electrodes);
    println!("Responsible-use note: synthetic educational data only.");
}
