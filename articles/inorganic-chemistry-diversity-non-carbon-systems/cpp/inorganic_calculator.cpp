#include <cmath>
#include <iomanip>
#include <iostream>

double oxidation_state(double total_charge, double known_contribution, double unknown_atom_count) {
    return (total_charge - known_contribution) / unknown_atom_count;
}

double cfse(double t2g_electrons, double eg_electrons, double delta_o) {
    return t2g_electrons * (-0.4 * delta_o) + eg_electrons * (0.6 * delta_o);
}

double spin_only_moment(double unpaired_electrons) {
    return std::sqrt(unpaired_electrons * (unpaired_electrons + 2.0));
}

double tolerance_factor(double r_a, double r_b, double r_x) {
    return (r_a + r_x) / (std::sqrt(2.0) * (r_b + r_x));
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "Mn_in_KMnO4_OS=" << oxidation_state(0.0, -7.0, 1.0) << "\n";
    std::cout << "octahedral_d3_CFSE=" << cfse(3.0, 0.0, 1.0) << "\n";
    std::cout << "spin_only_d3=" << spin_only_moment(3.0) << "\n";
    std::cout << "tolerance_factor=" << tolerance_factor(1.60, 0.60, 1.40) << "\n";
    return 0;
}
