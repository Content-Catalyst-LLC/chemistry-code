use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("colloid_systems.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read colloid systems data.");

    let mut system_types = BTreeSet::new();
    let mut dispersed_phases = BTreeSet::new();
    let mut row_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 11 {
            eprintln!("Malformed colloid row {}: expected 11 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        system_types.insert(fields[1].to_string());
        dispersed_phases.insert(fields[2].to_string());
        row_count += 1;
    }

    println!("Colloid soft matter manifest validation");
    println!("System rows: {}", row_count);
    println!("System types: {:?}", system_types);
    println!("Dispersed phases: {:?}", dispersed_phases);
    println!("Responsible-use note: synthetic educational data only.");
}
