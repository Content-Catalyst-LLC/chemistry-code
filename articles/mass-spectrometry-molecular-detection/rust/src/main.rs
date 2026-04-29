use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("ms_metadata.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read MS metadata.");

    let mut methods = BTreeSet::new();
    let mut analyzers = BTreeSet::new();
    let mut ionization_modes = BTreeSet::new();
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
        analyzers.insert(fields[3].to_string());
        ionization_modes.insert(fields[4].to_string());
        row_count += 1;
    }

    println!("Mass spectrometry manifest validation");
    println!("Metadata rows: {}", row_count);
    println!("Methods: {:?}", methods);
    println!("Analyzers: {:?}", analyzers);
    println!("Ionization modes: {:?}", ionization_modes);
    println!("Responsible-use note: synthetic educational data only.");
}
