#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

constexpr double H = 6.62607015e-34;
constexpr double C = 299792458.0;
constexpr double EV_TO_J = 1.602176634e-19;
constexpr double ELECTRON_MASS = 9.1093837139e-31;

double hydrogen_energy_ev(double n) {
    return -13.6 / (n * n);
}

double photon_wavelength_nm(double delta_energy_ev) {
    double delta_j = delta_energy_ev * EV_TO_J;
    return (H * C / delta_j) * 1.0e9;
}

double particle_in_box_energy_ev(double n, double box_length_nm) {
    double length_m = box_length_nm * 1.0e-9;
    double energy_j = (n * n * H * H) / (8.0 * ELECTRON_MASS * length_m * length_m);
    return energy_j / EV_TO_J;
}

int main() {
    double e1 = hydrogen_energy_ev(1.0);
    double e2 = hydrogen_energy_ev(2.0);
    double wavelength = photon_wavelength_nm(std::abs(e2 - e1));

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "hydrogen_n1_energy_eV=" << e1 << "\n";
    std::cout << "hydrogen_n2_energy_eV=" << e2 << "\n";
    std::cout << std::setprecision(3);
    std::cout << "n2_to_n1_wavelength_nm=" << wavelength << "\n";
    std::cout << std::setprecision(6);
    std::cout << "particle_box_n1_1nm_eV=" << particle_in_box_energy_ev(1.0, 1.0) << "\n";

    return 0;
}
