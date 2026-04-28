#include <math.h>
#include <stdio.h>

double weak_acid_hydronium(double ka, double concentration) {
    return (-ka + sqrt(pow(ka, 2.0) + 4.0 * ka * concentration)) / 2.0;
}

double ph_from_hydronium(double h) {
    return -log10(h);
}

double henderson_hasselbalch(double pka, double base, double acid) {
    return pka + log10(base / acid);
}

int main(void) {
    double h = weak_acid_hydronium(1.8e-5, 0.100);
    double ph = ph_from_hydronium(h);
    double buffer_ph = henderson_hasselbalch(4.76, 0.120, 0.100);

    printf("weak_acid_hydronium=%.8f\n", h);
    printf("weak_acid_pH=%.6f\n", ph);
    printf("buffer_pH=%.6f\n", buffer_ph);

    return 0;
}
