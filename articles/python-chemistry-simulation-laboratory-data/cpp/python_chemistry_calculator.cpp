#include <cmath>
#include <iomanip>
#include <iostream>

double unknown_concentration(double response, double slope, double intercept) {
    return (response - intercept) / slope;
}

double first_order_concentration(double c0, double k, double t) {
    return c0 * std::exp(-k * t);
}

double half_life_first_order(double k) {
    return std::log(2.0) / k;
}

double standard_error(double sd, double n) {
    return sd / std::sqrt(n);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "unknown_concentration_mM=" << unknown_concentration(0.95, 0.30, 0.02) << "\n";
    std::cout << "first_order_concentration_mM=" << first_order_concentration(10.0, 0.015, 100.0) << "\n";
    std::cout << "half_life_s=" << half_life_first_order(0.015) << "\n";
    std::cout << "standard_error=" << standard_error(0.03, 3.0) << "\n";
    return 0;
}
