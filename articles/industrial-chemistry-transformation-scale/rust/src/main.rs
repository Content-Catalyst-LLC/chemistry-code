use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("process_routes.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read process routes data.");

    let mut process_types = BTreeSet::new();
    let mut row_count = 0usize;
    let mut review_like_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 12 {
            eprintln!("Malformed route row {}: expected 12 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        process_types.insert(fields[1].to_string());

        let actual: f64 = fields[3].parse().unwrap_or(0.0);
        let waste: f64 = fields[4].parse().unwrap_or(0.0);
        let solvent: f64 = fields[5].parse().unwrap_or(0.0);
        let hazard: f64 = fields[9].parse().unwrap_or(0.0);
        let separation: f64 = fields[10].parse().unwrap_or(0.0);

        let e_factor = if actual > 0.0 { waste / actual } else { 999.0 };
        let solvent_intensity = if actual > 0.0 { solvent / actual } else { 999.0 };

        if e_factor > 1.0 || solvent_intensity > 2.0 || hazard > 0.60 || separation > 0.70 {
            review_like_count += 1;
        }

        row_count += 1;
    }

    println!("Industrial chemistry manifest validation");
    println!("Route rows: {}", row_count);
    println!("Process types: {:?}", process_types);
    println!("Review-like rows: {}", review_like_count);
    println!("Responsible-use note: synthetic educational data only.");
}
