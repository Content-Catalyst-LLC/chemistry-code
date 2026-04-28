#include <math.h>
#include <stdio.h>

const double R = 8.314462618;

double delta_g_from_qk(double q, double k, double temperature_k) {
    return R * temperature_k * log(q / k) / 1000.0;
}

void solve_isomerization(double k, double total, double *a_eq, double *b_eq) {
    *a_eq = total / (1.0 + k);
    *b_eq = total - *a_eq;
}

int main(void) {
    double a_eq;
    double b_eq;
    double delta_g;

    solve_isomerization(4.0, 1.0, &a_eq, &b_eq);
    delta_g = delta_g_from_qk(0.5, 4.0, 298.15);

    printf("A_eq=%.6f\n", a_eq);
    printf("B_eq=%.6f\n", b_eq);
    printf("delta_g_kj_mol=%.6f\n", delta_g);

    return 0;
}
