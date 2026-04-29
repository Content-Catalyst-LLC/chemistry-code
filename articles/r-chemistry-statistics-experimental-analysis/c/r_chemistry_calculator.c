#include <math.h>
#include <stdio.h>

double mean(const double values[], int n) {
    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += values[i];
    }
    return sum / n;
}

double sample_sd(const double values[], int n) {
    double xbar = mean(values, n);
    double ss = 0.0;
    for (int i = 0; i < n; i++) {
        ss += pow(values[i] - xbar, 2.0);
    }
    return sqrt(ss / (n - 1));
}

double standard_error(const double values[], int n) {
    return sample_sd(values, n) / sqrt((double)n);
}

double rsd_percent(const double values[], int n) {
    return 100.0 * sample_sd(values, n) / mean(values, n);
}

double unknown_concentration(double response, double slope, double intercept) {
    return (response - intercept) / slope;
}

int main(void) {
    double values[] = {1.02, 1.05, 0.99};
    int n = 3;

    printf("mean=%.6f\n", mean(values, n));
    printf("sample_sd=%.6f\n", sample_sd(values, n));
    printf("standard_error=%.6f\n", standard_error(values, n));
    printf("rsd_percent=%.6f\n", rsd_percent(values, n));
    printf("unknown_concentration=%.6f\n", unknown_concentration(0.95, 0.30, 0.02));
    return 0;
}
