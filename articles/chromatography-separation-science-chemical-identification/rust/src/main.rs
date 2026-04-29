use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("chromatography_metadata.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read chromatography metadata.");

    let mut methods = BTreeSet::new();
    let mut instruments = BTreeSet::new();
    let mut columns = BTreeSet::new();
    let mut row_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 9 {
            eprintln!("Malformed metadata row {}: expected 9 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        methods.insert(fields[1].to_string());
        instruments.insert(fields[2].to_string());
        columns.insert(fields[3].to_string());
        row_count += 1;
    }

    println!("Chromatography manifest validation");
    println!("Metadata rows: {}", row_count);
    println!("Methods: {:?}", methods);
    println!("Instruments: {:?}", instruments);
    println!("Columns: {:?}", columns);
    println!("Responsible-use note: synthetic educational data only.");
}
