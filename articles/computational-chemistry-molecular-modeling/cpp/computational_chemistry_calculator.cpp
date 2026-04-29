#include <cmath>
#include <iomanip>
#include <iostream>

double boltzmann_weight(double delta_e_kj_mol, double temperature_k) {
    constexpr double R = 8.314462618;
    return std::exp(-(delta_e_kj_mol * 1000.0) / (R * temperature_k));
}

double lennard_jones(double distance, double epsilon, double sigma) {
    double ratio = sigma / distance;
    return 4.0 * epsilon * (std::pow(ratio, 12.0) - std::pow(ratio, 6.0));
}

double tanimoto(double a, double b, double c) {
    return c / (a + b - c);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "boltzmann_weight=" << boltzmann_weight(2.5, 298.15) << "\n";
    std::cout << "lennard_jones=" << lennard_jones(1.12, 1.0, 1.0) << "\n";
    std::cout << "tanimoto=" << tanimoto(5.0, 4.0, 3.0) << "\n";
    return 0;
}
