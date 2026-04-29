#include <math.h>
#include <stdio.h>

double lennard_jones(double distance, double epsilon, double sigma) {
    double ratio = sigma / distance;
    return 4.0 * epsilon * (pow(ratio, 12.0) - pow(ratio, 6.0));
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

int main(void) {
    printf("new_position=%.6f\n", velocity_verlet_position(0.0, 0.05, 0.10, 0.5));
    printf("new_velocity=%.6f\n", velocity_update(0.05, 0.10, 0.5));
    printf("lj_energy=%.6f\n", lennard_jones(1.12, 1.0, 1.0));
    printf("diffusion_estimate=%.6f\n", diffusion_from_msd(4.21, 7.0));
    return 0;
}
