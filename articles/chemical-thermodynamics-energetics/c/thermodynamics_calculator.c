#include <math.h>
#include <stdio.h>

const double R = 8.314462618;

double gibbs_free_energy(double delta_h_kj_mol, double delta_s_j_mol_k, double temperature_k) {
    return delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0;
}

double equilibrium_constant(double delta_g_standard_kj_mol, double temperature_k) {
    return exp(-(delta_g_standard_kj_mol * 1000.0) / (R * temperature_k));
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

int main(void) {
    double dg = gibbs_free_energy(-80.0, -100.0, 298.15);
    double k = equilibrium_constant(dg, 298.15);
    double dh_cal = calorimetry_delta_h(100.0, 4.184, 6.2, 0.0500);

    printf("delta_g_kj_mol=%.6f\n", dg);
    printf("equilibrium_constant=%.6f\n", k);
    printf("calorimetry_delta_h_kj_mol=%.6f\n", dh_cal);

    return 0;
}
