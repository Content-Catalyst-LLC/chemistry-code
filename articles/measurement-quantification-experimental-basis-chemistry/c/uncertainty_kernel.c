#include <math.h>
#include <stdio.h>

// Compact uncertainty kernel for replicate measurements.

int main(void) {
    double values[] = {1.0032, 1.0028, 1.0035, 1.0030, 1.0029, 1.0034};
    int n = 6;

    double sum = 0.0;
    for (int i = 0; i < n; i++) {
        sum += values[i];
    }

    double mean = sum / n;

    double squared_diff_sum = 0.0;
    for (int i = 0; i < n; i++) {
        double diff = values[i] - mean;
        squared_diff_sum += diff * diff;
    }

    double sd = sqrt(squared_diff_sum / (n - 1));
    double rsd_percent = 100.0 * sd / mean;
    double standard_uncertainty = sd / sqrt((double)n);
    double expanded_uncertainty = 2.0 * standard_uncertainty;

    printf("mean=%.8f\n", mean);
    printf("standard_deviation=%.8f\n", sd);
    printf("rsd_percent=%.8f\n", rsd_percent);
    printf("expanded_uncertainty=%.8f\n", expanded_uncertainty);

    return 0;
}
