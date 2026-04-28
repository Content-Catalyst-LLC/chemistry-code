#include <iostream>
#include <iomanip>
#include <vector>

constexpr double AVOGADRO_CONSTANT = 6.02214076e23;

int neutron_number(int mass_number, int atomic_number) {
    return mass_number - atomic_number;
}

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

double amount_from_mass(double mass_g, double molar_mass_g_mol) {
    return mass_g / molar_mass_g_mol;
}

int main() {
    std::vector<double> chlorine_masses {34.96885268, 36.96590260};
    std::vector<double> chlorine_abundances {0.7576, 0.2424};

    double chlorine_mass = isotope_weighted_mass(chlorine_masses, chlorine_abundances);
    double water_moles = amount_from_mass(18.015, 18.015);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "chlorine_weighted_atomic_mass_u=" << chlorine_mass << "\n";
    std::cout << "carbon_14_neutron_number=" << neutron_number(14, 6) << "\n";
    std::cout << "water_amount_mol=" << water_moles << "\n";
    std::cout << std::scientific << "water_estimated_entities=" << water_moles * AVOGADRO_CONSTANT << "\n";

    return 0;
}
