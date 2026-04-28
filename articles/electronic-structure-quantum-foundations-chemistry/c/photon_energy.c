#include <stdio.h>
#include <math.h>

#define H 6.62607015e-34
#define C 299792458.0
#define EV_TO_J 1.602176634e-19
#define ELECTRON_MASS 9.1093837139e-31

double hydrogen_energy_ev(double n) {
    return -13.6 / (n * n);
}

double photon_wavelength_nm(double delta_energy_ev) {
    double delta_j = delta_energy_ev * EV_TO_J;
    return (H * C / delta_j) * 1.0e9;
}

double particle_in_box_energy_ev(double n, double box_length_nm) {
    double length_m = box_length_nm * 1.0e-9;
    double energy_j = (n * n * H * H) / (8.0 * ELECTRON_MASS * length_m * length_m);
    return energy_j / EV_TO_J;
}

int main(void) {
    double e1 = hydrogen_energy_ev(1.0);
    double e2 = hydrogen_energy_ev(2.0);
    double wavelength = photon_wavelength_nm(fabs(e2 - e1));

    printf("hydrogen_n1_energy_eV=%.6f\n", e1);
    printf("hydrogen_n2_energy_eV=%.6f\n", e2);
    printf("n2_to_n1_wavelength_nm=%.3f\n", wavelength);
    printf("particle_box_n1_1nm_eV=%.6f\n", particle_in_box_energy_ev(1.0, 1.0));

    return 0;
}
