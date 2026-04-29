#include <stdio.h>
#include <math.h>

int main(void) {
    double coreDiameterNm = 18.0;
    double hydrodynamicDiameterNm = 24.0;

    double surfaceAreaToVolume = 6.0 / coreDiameterNm;

    double kB = 1.380649e-23;
    double T = 298.15;
    double eta = 0.00089;

    double diffusion = kB * T / (3.0 * M_PI * eta * hydrodynamicDiameterNm * 1.0e-9);

    printf("Nanoscale metric utility\n");
    printf("Surface-area-to-volume nm^-1: %.8f\n", surfaceAreaToVolume);
    printf("Diffusion estimate m^2/s: %.12e\n", diffusion);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
