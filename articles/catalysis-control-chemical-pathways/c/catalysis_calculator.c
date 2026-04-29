#include <math.h>
#include <stdio.h>

const double R_CONST = 8.314462618;

double rate_enhancement(double delta_ea_kj_mol, double temperature_k) {
    return exp((delta_ea_kj_mol * 1000.0) / (R_CONST * temperature_k));
}

double turnover_number(double product_mol, double catalyst_mol) {
    return product_mol / catalyst_mol;
}

double turnover_frequency(double product_mol, double catalyst_mol, double time_s) {
    return turnover_number(product_mol, catalyst_mol) / time_s;
}

double langmuir_theta(double k, double p) {
    return (k * p) / (1.0 + k * p);
}

int main(void) {
    printf("rate_enhancement=%.6f\n", rate_enhancement(25.0, 298.15));
    printf("TON=%.6f\n", turnover_number(0.05, 0.0005));
    printf("TOF=%.8f\n", turnover_frequency(0.05, 0.0005, 3600.0));
    printf("theta=%.6f\n", langmuir_theta(1.5, 1.0));
    return 0;
}
