#include <stdio.h>
#include <math.h>

int main(void) {
    double observed_mz = 195.0878;
    double theoretical_mz = 195.08765;
    double isotope_spacing = 0.5002;

    double ppm_error = (observed_mz - theoretical_mz) / theoretical_mz * 1000000.0;
    int estimated_charge = (int)round(1.0 / isotope_spacing);

    printf("Mass spectrometry metric utility\n");
    printf("Observed m/z: %.6f\n", observed_mz);
    printf("Theoretical m/z: %.6f\n", theoretical_mz);
    printf("ppm error: %.6f\n", ppm_error);
    printf("Isotope spacing: %.6f\n", isotope_spacing);
    printf("Estimated charge: %d\n", estimated_charge);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
