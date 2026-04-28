#include <cmath>
#include <iomanip>
#include <iostream>
#include <utility>

constexpr double R = 8.314462618;

double delta_g_from_qk(double q, double k, double temperature_k) {
    return R * temperature_k * std::log(q / k) / 1000.0;
}

std::pair<double, double> solve_isomerization(double k, double total) {
    double a_eq = total / (1.0 + k);
    double b_eq = total - a_eq;
    return {a_eq, b_eq};
}

int main() {
    auto [a_eq, b_eq] = solve_isomerization(4.0, 1.0);
    double delta_g = delta_g_from_qk(0.5, 4.0, 298.15);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "A_eq=" << a_eq << "\n";
    std::cout << "B_eq=" << b_eq << "\n";
    std::cout << "delta_g_kj_mol=" << delta_g << "\n";

    return 0;
}
