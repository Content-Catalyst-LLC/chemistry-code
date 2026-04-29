#include <math.h>
#include <stdio.h>

double dose_response(double concentration, double ec50, double hill, double bottom, double top) {
    return bottom + (top - bottom) / (1.0 + pow(ec50 / concentration, hill));
}

double occupancy(double ligand, double kd) {
    return ligand / (kd + ligand);
}

double target_engagement(double signal_control, double signal_treated, double signal_max) {
    return (signal_control - signal_treated) / (signal_control - signal_max);
}

int main(void) {
    printf("response=%.6f\n", dose_response(1.0, 1.5, 1.2, 0.05, 1.0));
    printf("occupancy=%.6f\n", occupancy(2.0, 2.0));
    printf("target_engagement=%.6f\n", target_engagement(100.0, 55.0, 20.0));
    return 0;
}
