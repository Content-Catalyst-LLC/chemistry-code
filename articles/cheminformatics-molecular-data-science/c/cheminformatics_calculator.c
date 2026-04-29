#include <math.h>
#include <stdio.h>

double tanimoto(double a, double b, double c) {
    return c / (a + b - c);
}

double pic50(double ic50_nm) {
    double ic50_m = ic50_nm * 1.0e-9;
    return -log10(ic50_m);
}

double euclidean_distance_3(double x1, double x2, double x3, double y1, double y2, double y3) {
    return sqrt((x1 - y1) * (x1 - y1) + (x2 - y2) * (x2 - y2) + (x3 - y3) * (x3 - y3));
}

int main(void) {
    printf("tanimoto=%.6f\n", tanimoto(5.0, 4.0, 3.0));
    printf("pIC50=%.6f\n", pic50(50.0));
    printf("distance=%.6f\n", euclidean_distance_3(1.0, 2.0, 3.0, 1.5, 2.5, 4.0));
    return 0;
}
