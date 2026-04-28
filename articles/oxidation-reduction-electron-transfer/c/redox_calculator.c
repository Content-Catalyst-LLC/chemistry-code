#include <math.h>
#include <stdio.h>

const double R_CONST = 8.314462618;
const double F_CONST = 96485.33212;

double cell_potential(double e_cathode, double e_anode) {
    return e_cathode - e_anode;
}

double delta_g(double n, double e_cell) {
    return -n * F_CONST * e_cell / 1000.0;
}

double nernst(double e0, double n, double q, double temperature_k) {
    return e0 - (R_CONST * temperature_k / (n * F_CONST)) * log(q);
}

int main(void) {
    double e_cell = cell_potential(0.34, -0.76);
    double dg = delta_g(2.0, e_cell);
    double e_nonstandard = nernst(1.10, 2.0, 100.0, 298.15);

    printf("E_cell_standard_V=%.6f\n", e_cell);
    printf("delta_g_standard_kj_mol=%.6f\n", dg);
    printf("E_nonstandard_V=%.6f\n", e_nonstandard);

    return 0;
}
