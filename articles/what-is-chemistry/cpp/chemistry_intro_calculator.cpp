#include <cmath>
#include <iostream>

// Introductory chemistry calculator in C++.

double moles_from_mass(double mass_g, double molar_mass_g_mol) {
    return mass_g / molar_mass_g_mol;
}

double molarity(double moles, double volume_l) {
    return moles / volume_l;
}

double first_order_concentration(double initial, double rate_constant, double time) {
    return initial * std::exp(-rate_constant * time);
}

int main() {
    double moles = moles_from_mass(5.844, 58.44);
    double concentration = molarity(moles, 0.500);
    double remaining = first_order_concentration(1.0, 0.15, 10.0);

    std::cout << "moles=" << moles << std::endl;
    std::cout << "molarity_mol_l=" << concentration << std::endl;
    std::cout << "first_order_concentration=" << remaining << std::endl;

    return 0;
}
