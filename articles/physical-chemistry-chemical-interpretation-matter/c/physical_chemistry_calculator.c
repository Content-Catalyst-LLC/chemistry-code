#include <math.h>
#include <stdio.h>

const double R_CONST = 8.314462618;
const double F_CONST = 96485.33212;

double equilibrium_constant(double delta_g_kj_mol, double temperature_k) {
    return exp(-(delta_g_kj_mol * 1000.0) / (R_CONST * temperature_k));
}

double arrhenius(double a, double ea_kj_mol, double temperature_k) {
    return a * exp(-(ea_kj_mol * 1000.0) / (R_CONST * temperature_k));
}

double nernst(double e0, double n, double q, double temperature_k) {
    return e0 - (R_CONST * temperature_k / (n * F_CONST)) * log(q);
}

int main(void) {
    printf("K_demo=%.6f\n", equilibrium_constant(-20.0, 298.15));
    printf("k_demo=%.6e\n", arrhenius(1.0e12, 75.0, 298.15));
    printf("E_demo=%.6f\n", nernst(1.10, 2.0, 100.0, 298.15));
    return 0;
}
