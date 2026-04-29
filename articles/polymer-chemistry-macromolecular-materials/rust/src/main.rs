use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("polymer_candidates.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read polymer candidate data.");

    let mut classes = BTreeSet::new();
    let mut row_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 10 {
            eprintln!("Malformed polymer row {}: expected 10 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        classes.insert(fields[1].to_string());
        row_count += 1;
    }

    println!("Polymer manifest validation");
    println!("Candidate rows: {}", row_count);
    println!("Polymer classes: {:?}", classes);
    println!("Responsible-use note: synthetic educational data only.");
}
