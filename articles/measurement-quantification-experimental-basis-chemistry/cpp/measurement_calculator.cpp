#include <cmath>
#include <iostream>
#include <vector>

// Introductory measurement and quantification calculator in C++.

double moles_from_mass(double mass_g, double molar_mass_g_mol) {
    return mass_g / molar_mass_g_mol;
}

double concentration_mol_l(double moles, double volume_l) {
    return moles / volume_l;
}

double dilution_stock_volume(double c1, double c2, double v2) {
    return (c2 * v2) / c1;
}

int main() {
    double moles = moles_from_mass(5.844, 58.44);
    double concentration = concentration_mol_l(moles, 0.500);
    double stock_volume = dilution_stock_volume(1.0, 0.10, 100.0);

    std::cout << "moles=" << moles << std::endl;
    std::cout << "concentration_mol_l=" << concentration << std::endl;
    std::cout << "stock_volume_ml=" << stock_volume << std::endl;

    return 0;
}
