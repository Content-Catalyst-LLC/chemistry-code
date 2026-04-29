#include <stdio.h>
#include <math.h>

int main(void) {
    double kB = 1.380649e-23;
    double T = 298.15;
    double eta0 = 0.00089;
    double diameterNm = 80.0;
    double diameterM = diameterNm * 1.0e-9;
    double phi = 0.04;

    double diffusion = kB * T / (3.0 * M_PI * eta0 * diameterM);
    double einsteinRelativeViscosity = 1.0 + 2.5 * phi;

    printf("Colloid metric utility\n");
    printf("Diffusion estimate m^2/s: %.12e\n", diffusion);
    printf("Einstein relative viscosity: %.8f\n", einsteinRelativeViscosity);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
