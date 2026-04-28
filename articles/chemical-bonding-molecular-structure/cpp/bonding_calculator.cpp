#include <cmath>
#include <iomanip>
#include <iostream>
#include <array>

double distance_3d(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    double dx = a[0] - b[0];
    double dy = a[1] - b[1];
    double dz = a[2] - b[2];
    return std::sqrt(dx * dx + dy * dy + dz * dz);
}

double bond_order(double bonding_electrons, double antibonding_electrons) {
    return (bonding_electrons - antibonding_electrons) / 2.0;
}

double electronegativity_difference(double chi_a, double chi_b) {
    return std::abs(chi_a - chi_b);
}

int main() {
    std::array<double, 3> oxygen {0.0, 0.0, 0.0};
    std::array<double, 3> hydrogen {0.958, 0.0, 0.0};

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "oh_distance_angstrom=" << distance_3d(oxygen, hydrogen) << "\n";
    std::cout << "oh_delta_chi=" << electronegativity_difference(3.44, 2.20) << "\n";
    std::cout << "h2_bond_order=" << bond_order(2.0, 0.0) << "\n";

    return 0;
}
