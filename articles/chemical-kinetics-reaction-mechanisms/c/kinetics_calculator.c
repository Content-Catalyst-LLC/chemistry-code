#include <math.h>
#include <stdio.h>

const double R = 8.314462618;

double first_order_concentration(double c0, double k, double t) {
    return c0 * exp(-k * t);
}

double half_life_first_order(double k) {
    return log(2.0) / k;
}

double arrhenius_rate_constant(double a, double ea_j_mol, double temperature_k) {
    return a * exp(-ea_j_mol / (R * temperature_k));
}

int main(void) {
    printf("first_order_concentration_t20=%.6f\n", first_order_concentration(1.0, 0.15, 20.0));
    printf("first_order_half_life=%.6f\n", half_life_first_order(0.15));
    printf("arrhenius_k_310K=%.6f\n", arrhenius_rate_constant(1.0e7, 55000.0, 310.0));
    return 0;
}
