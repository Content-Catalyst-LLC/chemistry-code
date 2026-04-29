fn dbe(c: f64, h: f64, n: f64, x: f64) -> f64 {
    c - (h + x) / 2.0 + n / 2.0 + 1.0
}

fn polarity_score(heteroatoms: f64, donors: f64, acceptors: f64) -> f64 {
    heteroatoms + donors + acceptors
}

fn main() {
    println!("benzene_DBE={:.6}", dbe(6.0, 6.0, 0.0, 0.0));
    println!("acetic_acid_DBE={:.6}", dbe(2.0, 4.0, 0.0, 0.0));
    println!("polarity_score={:.6}", polarity_score(2.0, 1.0, 2.0));
}
