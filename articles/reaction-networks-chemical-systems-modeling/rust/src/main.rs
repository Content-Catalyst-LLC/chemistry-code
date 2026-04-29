fn simulate_network(k1: f64, k2: f64, k3: f64, k4: f64, dt: f64, total_time: f64) -> [f64; 5] {
    let mut a = 1.0;
    let mut b = 0.0;
    let mut c = 0.0;
    let mut d = 0.0;
    let mut e = 0.0;

    let mut t = 0.0;

    while t <= total_time {
        let r1 = k1 * a;
        let r2 = k2 * b;
        let r3 = k3 * a;
        let r4 = k4 * b;

        a = (a + (-r1 - r3) * dt).max(0.0);
        b = (b + (r1 - r2 - r4) * dt).max(0.0);
        c = (c + r2 * dt).max(0.0);
        d = (d + r3 * dt).max(0.0);
        e = (e + r4 * dt).max(0.0);

        t += dt;
    }

    [a, b, c, d, e]
}

fn main() {
    let result = simulate_network(0.20, 0.08, 0.05, 0.03, 0.25, 50.0);

    println!("A_final={:.6}", result[0]);
    println!("B_final={:.6}", result[1]);
    println!("C_final={:.6}", result[2]);
    println!("D_final={:.6}", result[3]);
    println!("E_final={:.6}", result[4]);
}
