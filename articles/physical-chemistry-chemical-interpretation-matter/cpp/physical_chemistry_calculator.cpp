#include <cmath>
#include <iomanip>
#include <iostream>

constexpr double R = 8.314462618;
constexpr double F = 96485.33212;

double equilibrium_constant(double delta_g_kj_mol, double temperature_k) {
    return std::exp(-(delta_g_kj_mol * 1000.0) / (R * temperature_k));
}

double arrhenius(double a, double ea_kj_mol, double temperature_k) {
    return a * std::exp(-(ea_kj_mol * 1000.0) / (R * temperature_k));
}

double nernst(double e0, double n, double q, double temperature_k) {
    return e0 - (R * temperature_k / (n * F)) * std::log(q);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "K_demo=" << equilibrium_constant(-20.0, 298.15) << "\n";
    std::cout << std::scientific << "k_demo=" << arrhenius(1.0e12, 75.0, 298.15) << "\n";
    std::cout << std::fixed << "E_demo=" << nernst(1.10, 2.0, 100.0, 298.15) << "\n";
    return 0;
}
