#include <cmath>
#include <iomanip>
#include <iostream>

constexpr double R = 8.314462618;

double first_order_concentration(double c0, double k, double t) {
    return c0 * std::exp(-k * t);
}

double half_life_first_order(double k) {
    return std::log(2.0) / k;
}

double arrhenius_rate_constant(double a, double ea_j_mol, double temperature_k) {
    return a * std::exp(-ea_j_mol / (R * temperature_k));
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "first_order_concentration_t20=" << first_order_concentration(1.0, 0.15, 20.0) << "\n";
    std::cout << "first_order_half_life=" << half_life_first_order(0.15) << "\n";
    std::cout << "arrhenius_k_310K=" << arrhenius_rate_constant(1.0e7, 55000.0, 310.0) << "\n";
    return 0;
}
