#include <math.h>
#include <stdio.h>

double boltzmann_weight(double delta_e_kj_mol, double temperature_k) {
    const double R = 8.314462618;
    return exp(-(delta_e_kj_mol * 1000.0) / (R * temperature_k));
}

double lennard_jones(double distance, double epsilon, double sigma) {
    double ratio = sigma / distance;
    return 4.0 * epsilon * (pow(ratio, 12.0) - pow(ratio, 6.0));
}

double tanimoto(double a, double b, double c) {
    return c / (a + b - c);
}

int main(void) {
    printf("boltzmann_weight=%.6f\n", boltzmann_weight(2.5, 298.15));
    printf("lennard_jones=%.6f\n", lennard_jones(1.12, 1.0, 1.0));
    printf("tanimoto=%.6f\n", tanimoto(5.0, 4.0, 3.0));
    return 0;
}
