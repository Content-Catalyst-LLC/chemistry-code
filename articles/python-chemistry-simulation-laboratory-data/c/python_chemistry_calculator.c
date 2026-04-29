#include <math.h>
#include <stdio.h>

double unknown_concentration(double response, double slope, double intercept) {
    return (response - intercept) / slope;
}

double first_order_concentration(double c0, double k, double t) {
    return c0 * exp(-k * t);
}

double half_life_first_order(double k) {
    return log(2.0) / k;
}

double standard_error(double sd, double n) {
    return sd / sqrt(n);
}

int main(void) {
    printf("unknown_concentration_mM=%.6f\n", unknown_concentration(0.95, 0.30, 0.02));
    printf("first_order_concentration_mM=%.6f\n", first_order_concentration(10.0, 0.015, 100.0));
    printf("half_life_s=%.6f\n", half_life_first_order(0.015));
    printf("standard_error=%.6f\n", standard_error(0.03, 3.0));
    return 0;
}
