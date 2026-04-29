#include <math.h>
#include <stdio.h>

double michaelis_menten(double substrate, double vmax, double km) {
    return vmax * substrate / (km + substrate);
}

double occupancy(double ligand, double kd) {
    return ligand / (kd + ligand);
}

double hill_occupancy(double ligand, double kd, double n) {
    return pow(ligand, n) / (pow(kd, n) + pow(ligand, n));
}

double delta_g_standard(double k, double temperature_k) {
    const double R = 8.314462618;
    return -(R * temperature_k * log(k)) / 1000.0;
}

int main(void) {
    printf("velocity=%.6f\n", michaelis_menten(5.0, 120.0, 3.5));
    printf("occupancy=%.6f\n", occupancy(2.0, 2.0));
    printf("hill_occupancy=%.6f\n", hill_occupancy(2.0, 2.0, 2.0));
    printf("delta_g_kj_mol=%.6f\n", delta_g_standard(1000.0, 298.15));
    return 0;
}
