#include <math.h>
#include <stdio.h>

double oxidation_state(double total_charge, double known_contribution, double unknown_atom_count) {
    return (total_charge - known_contribution) / unknown_atom_count;
}

double cfse(double t2g_electrons, double eg_electrons, double delta_o) {
    return t2g_electrons * (-0.4 * delta_o) + eg_electrons * (0.6 * delta_o);
}

double spin_only_moment(double unpaired_electrons) {
    return sqrt(unpaired_electrons * (unpaired_electrons + 2.0));
}

double tolerance_factor(double r_a, double r_b, double r_x) {
    return (r_a + r_x) / (sqrt(2.0) * (r_b + r_x));
}

int main(void) {
    printf("Mn_in_KMnO4_OS=%.6f\n", oxidation_state(0.0, -7.0, 1.0));
    printf("octahedral_d3_CFSE=%.6f\n", cfse(3.0, 0.0, 1.0));
    printf("spin_only_d3=%.6f\n", spin_only_moment(3.0));
    printf("tolerance_factor=%.6f\n", tolerance_factor(1.60, 0.60, 1.40));
    return 0;
}
