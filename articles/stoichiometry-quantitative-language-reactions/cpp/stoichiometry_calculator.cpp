#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double limiting_extent(const std::vector<double>& available, const std::vector<double>& coefficients) {
    double minimum = std::numeric_limits<double>::infinity();

    for (std::size_t i = 0; i < available.size(); ++i) {
        minimum = std::min(minimum, available[i] / coefficients[i]);
    }

    return minimum;
}

double percent_yield(double actual, double theoretical) {
    return actual / theoretical * 100.0;
}

double dilution_volume(double c1, double c2, double v2) {
    return (c2 * v2) / c1;
}

int main() {
    double extent = limiting_extent({4.0, 1.5}, {2.0, 1.0});
    double water_mol = extent * 2.0;
    double theoretical_yield = water_mol * 18.01528;

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "maximum_extent_mol=" << extent << "\n";
    std::cout << "water_mol_theoretical=" << water_mol << "\n";
    std::cout << "theoretical_yield_g=" << theoretical_yield << "\n";
    std::cout << "percent_yield=" << percent_yield(45.0, theoretical_yield) << "\n";
    std::cout << "stock_volume_L=" << dilution_volume(1.0, 0.1, 0.25) << "\n";

    return 0;
}
