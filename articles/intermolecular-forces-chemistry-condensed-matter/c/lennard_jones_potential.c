#include <stdio.h>
#include <math.h>

double lennard_jones(double r_angstrom, double epsilon_kj_mol, double sigma_angstrom) {
    double ratio = sigma_angstrom / r_angstrom;
    return 4.0 * epsilon_kj_mol * (pow(ratio, 12.0) - pow(ratio, 6.0));
}

double coulomb_relative(double q1, double q2, double r) {
    return q1 * q2 / r;
}

int main(void) {
    double epsilon = 0.997;
    double sigma = 3.40;
    double r_min = pow(2.0, 1.0 / 6.0) * sigma;
    double u_min = lennard_jones(r_min, epsilon, sigma);

    printf("r_min_angstrom=%.6f\n", r_min);
    printf("u_min_kj_mol=%.6f\n", u_min);
    printf("relative_coulomb_attraction=%.6f\n", coulomb_relative(1.0, -1.0, 2.0));

    return 0;
}
