#include <math.h>
#include <stdio.h>

// Compact first-order kinetics kernel.

int main(void) {
    double initial_concentration = 1.0;
    double rate_constant = 0.15;

    for (int time = 0; time <= 20; time += 5) {
        double concentration = initial_concentration * exp(-rate_constant * time);
        printf("time_min=%d concentration_mol_l=%.6f\n", time, concentration);
    }

    return 0;
}
