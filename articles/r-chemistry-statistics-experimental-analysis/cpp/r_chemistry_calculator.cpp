#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

double mean(const std::vector<double>& values) {
    return std::accumulate(values.begin(), values.end(), 0.0) / values.size();
}

double sample_sd(const std::vector<double>& values) {
    double xbar = mean(values);
    double ss = 0.0;
    for (double value : values) {
        ss += std::pow(value - xbar, 2.0);
    }
    return std::sqrt(ss / static_cast<double>(values.size() - 1));
}

double standard_error(const std::vector<double>& values) {
    return sample_sd(values) / std::sqrt(static_cast<double>(values.size()));
}

double rsd_percent(const std::vector<double>& values) {
    return 100.0 * sample_sd(values) / mean(values);
}

double unknown_concentration(double response, double slope, double intercept) {
    return (response - intercept) / slope;
}

int main() {
    std::vector<double> values = {1.02, 1.05, 0.99};

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "mean=" << mean(values) << "\n";
    std::cout << "sample_sd=" << sample_sd(values) << "\n";
    std::cout << "standard_error=" << standard_error(values) << "\n";
    std::cout << "rsd_percent=" << rsd_percent(values) << "\n";
    std::cout << "unknown_concentration=" << unknown_concentration(0.95, 0.30, 0.02) << "\n";
    return 0;
}
