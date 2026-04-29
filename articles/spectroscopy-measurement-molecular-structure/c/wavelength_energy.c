#include <stdio.h>

int main(void) {
    const double h = 6.62607015e-34;
    const double c = 299792458.0;
    const double avogadro = 6.02214076e23;

    double wavelength_nm = 520.0;
    double wavelength_m = wavelength_nm * 1e-9;
    double energy_j = h * c / wavelength_m;
    double energy_kj_mol = energy_j * avogadro / 1000.0;

    printf("Spectral wavelength-energy conversion\n");
    printf("Wavelength nm: %.3f\n", wavelength_nm);
    printf("Photon energy kJ/mol: %.6f\n", energy_kj_mol);
    printf("Responsible-use note: synthetic educational conversion only.\n");

    return 0;
}
