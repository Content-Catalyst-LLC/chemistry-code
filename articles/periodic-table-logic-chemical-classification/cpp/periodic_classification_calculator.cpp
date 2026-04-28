#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double isotope_weighted_mass(
    const std::vector<double>& masses,
    const std::vector<double>& abundances
) {
    double total = 0.0;
    for (std::size_t i = 0; i < masses.size(); ++i) {
        total += masses[i] * abundances[i];
    }
    return total;
}

int neutron_number(int mass_number, int atomic_number) {
    return mass_number - atomic_number;
}

double feature_distance(
    const std::vector<double>& a,
    const std::vector<double>& b
) {
    double total = 0.0;
    for (std::size_t i = 0; i < a.size(); ++i) {
        double delta = a[i] - b[i];
        total += delta * delta;
    }
    return std::sqrt(total);
}

int main() {
    double chlorine_mass = isotope_weighted_mass(
        {34.96885268, 36.96590260},
        {0.7576, 0.2424}
    );

    double distance = feature_distance(
        {1.0, 2.0, 128.0, 520.0},
        {1.0, 3.0, 166.0, 496.0}
    );

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "chlorine_weighted_atomic_mass_u=" << chlorine_mass << "\n";
    std::cout << "carbon_13_neutron_number=" << neutron_number(13, 6) << "\n";
    std::cout << "li_na_feature_distance_unscaled=" << distance << "\n";

    return 0;
}
