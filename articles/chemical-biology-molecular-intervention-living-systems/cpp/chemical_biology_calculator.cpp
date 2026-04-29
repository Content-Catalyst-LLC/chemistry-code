#include <cmath>
#include <iomanip>
#include <iostream>

double dose_response(double concentration, double ec50, double hill, double bottom, double top) {
    return bottom + (top - bottom) / (1.0 + std::pow(ec50 / concentration, hill));
}

double occupancy(double ligand, double kd) {
    return ligand / (kd + ligand);
}

double target_engagement(double signal_control, double signal_treated, double signal_max) {
    return (signal_control - signal_treated) / (signal_control - signal_max);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "response=" << dose_response(1.0, 1.5, 1.2, 0.05, 1.0) << "\n";
    std::cout << "occupancy=" << occupancy(2.0, 2.0) << "\n";
    std::cout << "target_engagement=" << target_engagement(100.0, 55.0, 20.0) << "\n";
    return 0;
}
