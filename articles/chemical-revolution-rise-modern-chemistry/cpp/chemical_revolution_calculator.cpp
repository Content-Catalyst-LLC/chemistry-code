#include <iostream>

// Introductory Chemical Revolution calculator in C++.

double oxide_mass(double metal_mass_g, double oxygen_mass_g) {
    return metal_mass_g + oxygen_mass_g;
}

double oxygen_mass_fraction(double metal_mass_g, double oxygen_mass_g) {
    return oxygen_mass_g / oxide_mass(metal_mass_g, oxygen_mass_g);
}

double mass_difference(double reactant_mass_g, double product_mass_g) {
    return product_mass_g - reactant_mass_g;
}

int main() {
    std::cout << "magnesium_oxide_mass_g=" << oxide_mass(24.305, 16.000) << std::endl;
    std::cout << "oxygen_mass_fraction=" << oxygen_mass_fraction(24.305, 16.000) << std::endl;
    std::cout << "mass_difference_closed_system=" << mass_difference(44.0, 44.0) << std::endl;

    return 0;
}
