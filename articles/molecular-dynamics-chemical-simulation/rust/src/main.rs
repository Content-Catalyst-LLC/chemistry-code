fn lennard_jones(distance: f64, epsilon: f64, sigma: f64) -> f64 {
    let ratio = sigma / distance;
    4.0 * epsilon * (ratio.powi(12) - ratio.powi(6))
}

fn velocity_verlet_position(position: f64, velocity: f64, acceleration: f64, dt: f64) -> f64 {
    position + velocity * dt + 0.5 * acceleration * dt.powi(2)
}

fn velocity_update(velocity: f64, acceleration: f64, dt: f64) -> f64 {
    velocity + acceleration * dt
}

fn diffusion_from_msd(msd: f64, time: f64) -> f64 {
    msd / (6.0 * time)
}

fn main() {
    println!("new_position={:.6}", velocity_verlet_position(0.0, 0.05, 0.10, 0.5));
    println!("new_velocity={:.6}", velocity_update(0.05, 0.10, 0.5));
    println!("lj_energy={:.6}", lennard_jones(1.12, 1.0, 1.0));
    println!("diffusion_estimate={:.6}", diffusion_from_msd(4.21, 7.0));
}
