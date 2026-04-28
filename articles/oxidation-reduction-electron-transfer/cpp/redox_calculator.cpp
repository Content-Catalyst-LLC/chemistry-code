#include <cmath>
#include <iomanip>
#include <iostream>

constexpr double R = 8.314462618;
constexpr double F = 96485.33212;

double cell_potential(double e_cathode, double e_anode) {
    return e_cathode - e_anode;
}

double delta_g(double n, double e_cell) {
    return -n * F * e_cell / 1000.0;
}

double nernst(double e0, double n, double q, double temperature_k) {
    return e0 - (R * temperature_k / (n * F)) * std::log(q);
}

int main() {
    double e_cell = cell_potential(0.34, -0.76);
    double dg = delta_g(2.0, e_cell);
    double e_nonstandard = nernst(1.10, 2.0, 100.0, 298.15);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "E_cell_standard_V=" << e_cell << "\n";
    std::cout << "delta_g_standard_kj_mol=" << dg << "\n";
    std::cout << "E_nonstandard_V=" << e_nonstandard << "\n";

    return 0;
}
