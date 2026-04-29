#include <stdio.h>

int main(void) {
    double wavelength_nm = 800.0;
    double photon_energy_eV = 1240.0 / wavelength_nm;

    double q = 1.602176634e-19;
    double electron_concentration = 1.0e16;
    double hole_concentration = 1.0e15;
    double electron_mobility = 35.0;
    double hole_mobility = 20.0;

    double conductivity_proxy = q * (
        electron_concentration * electron_mobility +
        hole_concentration * hole_mobility
    );

    printf("Photon and transport metric utility\n");
    printf("Photon energy estimate eV: %.8f\n", photon_energy_eV);
    printf("Conductivity proxy: %.12e\n", conductivity_proxy);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
