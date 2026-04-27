#include <cmath>
#include <iostream>
#include <vector>

// Introductory mathematical chemistry calculator in C++.

double first_order_concentration(double initial, double rate_constant, double time) {
    return initial * std::exp(-rate_constant * time);
}

double equilibrium_constant(double delta_g_standard_kj_mol, double temperature_k) {
    const double r = 8.314462618;
    return std::exp(-(delta_g_standard_kj_mol * 1000.0) / (r * temperature_k));
}

double distance(const std::vector<double>& a, const std::vector<double>& b) {
    double sumsq = 0.0;
    for (std::size_t i = 0; i < a.size(); ++i) {
        double diff = a[i] - b[i];
        sumsq += diff * diff;
    }
    return std::sqrt(sumsq);
}

int main() {
    double concentration = first_order_concentration(1.0, 0.15, 10.0);
    double k_eq = equilibrium_constant(-5.0, 298.15);
    double d_oh = distance({0.0, 0.0, 0.0}, {0.958, 0.0, 0.0});

    std::cout << "first_order_concentration_t10=" << concentration << std::endl;
    std::cout << "equilibrium_constant=" << k_eq << std::endl;
    std::cout << "distance_oh_angstrom=" << d_oh << std::endl;

    return 0;
}
