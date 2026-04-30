/*
Circular Chemistry, Waste, and Material Futures
C circular chemistry metric kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double recovery_yield(double recovered, double input) {
    if (input <= 0.0) return 0.0;
    return recovered / input;
}

double circular_retention(double recovery, double quality, double substitution) {
    return recovery * quality * substitution;
}

double material_remaining(double initial_mass, double loss_fraction, int cycles) {
    return initial_mass * pow(1.0 - loss_fraction, cycles);
}

double hazard_weighted_flow(double recovered, double hazard, double exposure) {
    return recovered * hazard * exposure;
}

double energy_intensity(double energy, double recovered) {
    if (recovered <= 0.0) return 0.0;
    return energy / recovered;
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_circular_chemistry_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_circular_chemistry_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "stream,recovery_yield,circular_retention,material_remaining_after_cycles,hazard_weighted_flow,energy_intensity\n");

    double rec = recovery_yield(760.0, 1000.0);
    fprintf(fp, "PET_bottles_clear,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        rec,
        circular_retention(rec, 0.82, 0.72),
        material_remaining(1000.0, 0.12, 3),
        hazard_weighted_flow(760.0, 0.18, 0.22),
        energy_intensity(180.0, 760.0)
    );

    rec = recovery_yield(310.0, 500.0);
    fprintf(fp, "Lithium_ion_batteries,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        rec,
        circular_retention(rec, 0.78, 0.72),
        material_remaining(500.0, 0.18, 2),
        hazard_weighted_flow(310.0, 0.48, 0.55),
        energy_intensity(520.0, 310.0)
    );

    fclose(fp);
    printf("C circular chemistry kernels complete.\n");
    return 0;
}
