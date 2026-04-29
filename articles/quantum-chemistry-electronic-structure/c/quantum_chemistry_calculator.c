#include <math.h>
#include <stdio.h>

double boltzmann_weight(double delta_e_kj_mol, double temperature_k) {
    const double R = 8.314462618;
    return exp(-(delta_e_kj_mol * 1000.0) / (R * temperature_k));
}

double tst_rate(double delta_g_dagger_kj_mol, double temperature_k) {
    const double kB = 1.380649e-23;
    const double h = 6.62607015e-34;
    const double R = 8.314462618;
    return (kB * temperature_k / h) *
           exp(-(delta_g_dagger_kj_mol * 1000.0) / (R * temperature_k));
}

void two_level_energies(double ea, double eb, double v, double *e1, double *e2) {
    double trace = ea + eb;
    double diff = ea - eb;
    double split = sqrt(diff * diff + 4.0 * v * v);
    *e1 = (trace - split) / 2.0;
    *e2 = (trace + split) / 2.0;
}

int main(void) {
    double e1, e2;
    two_level_energies(-10.0, -8.0, -2.0, &e1, &e2);

    printf("two_level_E1=%.6f\n", e1);
    printf("two_level_E2=%.6f\n", e2);
    printf("boltzmann_weight=%.10f\n", boltzmann_weight(25.0, 298.15));
    printf("tst_rate=%.6e\n", tst_rate(50.0, 298.15));
    return 0;
}
