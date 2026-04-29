#include <cmath>
#include <iomanip>
#include <iostream>

double lennard_jones(double distance, double epsilon, double sigma) {
    double ratio = sigma / distance;
    return 4.0 * epsilon * (std::pow(ratio, 12.0) - std::pow(ratio, 6.0));
}

double velocity_verlet_position(double position, double velocity, double acceleration, double dt) {
    return position + velocity * dt + 0.5 * acceleration * dt * dt;
}

double velocity_update(double velocity, double acceleration, double dt) {
    return velocity + acceleration * dt;
}

double diffusion_from_msd(double msd, double time) {
    return msd / (6.0 * time);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "new_position=" << velocity_verlet_position(0.0, 0.05, 0.10, 0.5) << "\n";
    std::cout << "new_velocity=" << velocity_update(0.05, 0.10, 0.5) << "\n";
    std::cout << "lj_energy=" << lennard_jones(1.12, 1.0, 1.0) << "\n";
    std::cout << "diffusion_estimate=" << diffusion_from_msd(4.21, 7.0) << "\n";
    return 0;
}
