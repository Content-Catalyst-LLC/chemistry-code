#include <cmath>
#include <iostream>
#include <vector>

// Introductory chemical metrology calculator in C++.

double combined_standard_uncertainty(const std::vector<double>& components) {
    double sumsq = 0.0;
    for (double component : components) {
        sumsq += component * component;
    }
    return std::sqrt(sumsq);
}

double normalized_error(double x_lab, double x_ref, double u_lab, double u_ref) {
    return (x_lab - x_ref) / std::sqrt(u_lab * u_lab + u_ref * u_ref);
}

int main() {
    std::vector<double> components = {0.004, 0.006, 0.010, 0.015, 0.012, 0.020};

    double uc = combined_standard_uncertainty(components);
    double expanded = 2.0 * uc;
    double en = normalized_error(10.2, 10.0, 0.8, 0.4);

    std::cout << "combined_standard_uncertainty=" << uc << std::endl;
    std::cout << "expanded_uncertainty=" << expanded << std::endl;
    std::cout << "normalized_error=" << en << std::endl;

    return 0;
}
