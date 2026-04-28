#include <cmath>
#include <iomanip>
#include <iostream>

constexpr double R = 8.314462618;

double gibbs_free_energy(double delta_h_kj_mol, double delta_s_j_mol_k, double temperature_k) {
    return delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0;
}

double equilibrium_constant(double delta_g_standard_kj_mol, double temperature_k) {
    return std::exp(-(delta_g_standard_kj_mol * 1000.0) / (R * temperature_k));
}

double calorimetry_delta_h(
    double mass_g,
    double specific_heat_j_g_k,
    double delta_t_k,
    double amount_mol
) {
    double q_solution_j = mass_g * specific_heat_j_g_k * delta_t_k;
    double q_reaction_j = -q_solution_j;
    return q_reaction_j / 1000.0 / amount_mol;
}

int main() {
    double dg = gibbs_free_energy(-80.0, -100.0, 298.15);
    double k = equilibrium_constant(dg, 298.15);
    double dh_cal = calorimetry_delta_h(100.0, 4.184, 6.2, 0.0500);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "delta_g_kj_mol=" << dg << "\n";
    std::cout << "equilibrium_constant=" << k << "\n";
    std::cout << "calorimetry_delta_h_kj_mol=" << dh_cal << "\n";

    return 0;
}
