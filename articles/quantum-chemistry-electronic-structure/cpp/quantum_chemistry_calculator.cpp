#include <cmath>
#include <iomanip>
#include <iostream>
#include <utility>

double boltzmann_weight(double delta_e_kj_mol, double temperature_k) {
    constexpr double R = 8.314462618;
    return std::exp(-(delta_e_kj_mol * 1000.0) / (R * temperature_k));
}

double tst_rate(double delta_g_dagger_kj_mol, double temperature_k) {
    constexpr double kB = 1.380649e-23;
    constexpr double h = 6.62607015e-34;
    constexpr double R = 8.314462618;
    return (kB * temperature_k / h) *
           std::exp(-(delta_g_dagger_kj_mol * 1000.0) / (R * temperature_k));
}

std::pair<double, double> two_level_energies(double ea, double eb, double v) {
    double trace = ea + eb;
    double diff = ea - eb;
    double split = std::sqrt(diff * diff + 4.0 * v * v);
    return {(trace - split) / 2.0, (trace + split) / 2.0};
}

int main() {
    auto [e1, e2] = two_level_energies(-10.0, -8.0, -2.0);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "two_level_E1=" << e1 << "\n";
    std::cout << "two_level_E2=" << e2 << "\n";
    std::cout << std::setprecision(10);
    std::cout << "boltzmann_weight=" << boltzmann_weight(25.0, 298.15) << "\n";
    std::cout << std::scientific << "tst_rate=" << tst_rate(50.0, 298.15) << "\n";

    return 0;
}
