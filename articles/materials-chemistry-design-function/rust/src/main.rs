use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("material_candidates.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read materials candidate data.");

    let mut material_classes = BTreeSet::new();
    let mut row_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 8 {
            eprintln!("Malformed materials row {}: expected 8 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        material_classes.insert(fields[1].to_string());
        row_count += 1;
    }

    println!("Materials design manifest validation");
    println!("Candidate rows: {}", row_count);
    println!("Material classes: {:?}", material_classes);
    println!("Responsible-use note: synthetic educational data only.");
}
