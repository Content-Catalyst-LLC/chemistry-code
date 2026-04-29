use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

fn main() {
    let base = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..");
    let data_path = base.join("data").join("cell_candidates.csv");

    let content = fs::read_to_string(&data_path)
        .expect("Could not read cell candidate data.");

    let mut chemistries = BTreeSet::new();
    let mut row_count = 0usize;
    let mut review_like_count = 0usize;

    for (index, line) in content.lines().enumerate() {
        if index == 0 {
            continue;
        }

        let fields: Vec<&str> = line.split(',').collect();

        if fields.len() != 10 {
            eprintln!("Malformed cell row {}: expected 10 fields, found {}", index + 1, fields.len());
            std::process::exit(1);
        }

        chemistries.insert(fields[1].to_string());

        let critical_score: f64 = fields[8].parse().unwrap_or(0.0);
        let safety_score: f64 = fields[9].parse().unwrap_or(0.0);

        if critical_score > 0.60 || safety_score > 0.40 {
            review_like_count += 1;
        }

        row_count += 1;
    }

    println!("Electrochemistry energy-storage manifest validation");
    println!("Candidate rows: {}", row_count);
    println!("Chemistries: {:?}", chemistries);
    println!("Critical/safety review-like rows: {}", review_like_count);
    println!("Responsible-use note: synthetic educational data only.");
}
