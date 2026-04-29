#include <stdio.h>

double concentration_from_calibration(double signal, double slope, double intercept) {
    return (signal - intercept) / slope;
}

double lod(double blank_sd, double slope) {
    return 3.0 * blank_sd / slope;
}

double loq(double blank_sd, double slope) {
    return 10.0 * blank_sd / slope;
}

double chromatographic_resolution(double tr1, double tr2, double w1, double w2) {
    return 2.0 * (tr2 - tr1) / (w1 + w2);
}

double beer_lambert_concentration(double absorbance, double epsilon, double path_length) {
    return absorbance / (epsilon * path_length);
}

int main(void) {
    printf("unknown_concentration=%.6f\n", concentration_from_calibration(3.72, 0.515, 0.04));
    printf("LOD=%.6f\n", lod(0.0032, 0.515));
    printf("LOQ=%.6f\n", loq(0.0032, 0.515));
    printf("resolution=%.6f\n", chromatographic_resolution(3.10, 5.20, 0.42, 0.50));
    printf("beer_lambert_c=%.8f\n", beer_lambert_concentration(0.625, 12500.0, 1.0));
    return 0;
}
