#include <cmath>
#include <iomanip>
#include <iostream>

constexpr double R = 8.314462618;

double rate_enhancement(double delta_ea_kj_mol, double temperature_k) {
    return std::exp((delta_ea_kj_mol * 1000.0) / (R * temperature_k));
}

double turnover_number(double product_mol, double catalyst_mol) {
    return product_mol / catalyst_mol;
}

double turnover_frequency(double product_mol, double catalyst_mol, double time_s) {
    return turnover_number(product_mol, catalyst_mol) / time_s;
}

double langmuir_theta(double k, double p) {
    return (k * p) / (1.0 + k * p);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "rate_enhancement=" << rate_enhancement(25.0, 298.15) << "\n";
    std::cout << "TON=" << turnover_number(0.05, 0.0005) << "\n";
    std::cout << std::setprecision(8);
    std::cout << "TOF=" << turnover_frequency(0.05, 0.0005, 3600.0) << "\n";
    std::cout << std::setprecision(6);
    std::cout << "theta=" << langmuir_theta(1.5, 1.0) << "\n";
    return 0;
}
