#include <cmath>
#include <iomanip>
#include <iostream>

double weak_acid_hydronium(double ka, double concentration) {
    return (-ka + std::sqrt(std::pow(ka, 2.0) + 4.0 * ka * concentration)) / 2.0;
}

double ph_from_hydronium(double h) {
    return -std::log10(h);
}

double henderson_hasselbalch(double pka, double base, double acid) {
    return pka + std::log10(base / acid);
}

int main() {
    double h = weak_acid_hydronium(1.8e-5, 0.100);
    double ph = ph_from_hydronium(h);
    double buffer_ph = henderson_hasselbalch(4.76, 0.120, 0.100);

    std::cout << std::fixed << std::setprecision(8);
    std::cout << "weak_acid_hydronium=" << h << "\n";
    std::cout << std::setprecision(6);
    std::cout << "weak_acid_pH=" << ph << "\n";
    std::cout << "buffer_pH=" << buffer_ph << "\n";

    return 0;
}
