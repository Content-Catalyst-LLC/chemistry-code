fn distance(a: [f64; 3], b: [f64; 3]) -> f64 {
    let dx = a[0] - b[0];
    let dy = a[1] - b[1];
    let dz = a[2] - b[2];
    (dx * dx + dy * dy + dz * dz).sqrt()
}

fn dot(a: [f64; 3], b: [f64; 3]) -> f64 {
    a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
}

fn subtract(a: [f64; 3], b: [f64; 3]) -> [f64; 3] {
    [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
}

fn angle_degrees(a: [f64; 3], b: [f64; 3], c: [f64; 3]) -> f64 {
    let u = subtract(a, b);
    let v = subtract(c, b);
    let cos_theta = dot(u, v) / (dot(u, u).sqrt() * dot(v, v).sqrt());
    cos_theta.clamp(-1.0, 1.0).acos() * 180.0 / std::f64::consts::PI
}

fn main() {
    let oxygen = [0.0, 0.0, 0.0];
    let h1 = [0.958, 0.0, 0.0];
    let h2 = [-0.239, 0.927, 0.0];

    println!("OH distance angstrom={:.6}", distance(oxygen, h1));
    println!("HOH angle degrees={:.3}", angle_degrees(h1, oxygen, h2));
}
