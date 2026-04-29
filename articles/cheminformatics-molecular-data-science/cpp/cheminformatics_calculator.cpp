#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double tanimoto(double a, double b, double c) {
    return c / (a + b - c);
}

double pic50(double ic50_nm) {
    double ic50_m = ic50_nm * 1.0e-9;
    return -std::log10(ic50_m);
}

double euclidean_distance(const std::vector<double>& x, const std::vector<double>& y) {
    double sum = 0.0;
    for (std::size_t i = 0; i < x.size(); ++i) {
        double delta = x[i] - y[i];
        sum += delta * delta;
    }
    return std::sqrt(sum);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "tanimoto=" << tanimoto(5.0, 4.0, 3.0) << "\n";
    std::cout << "pIC50=" << pic50(50.0) << "\n";
    std::cout << "distance=" << euclidean_distance({1.0, 2.0, 3.0}, {1.5, 2.5, 4.0}) << "\n";
    return 0;
}
