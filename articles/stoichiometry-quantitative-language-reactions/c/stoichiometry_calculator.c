#include <math.h>
#include <stdio.h>

double limiting_extent(double available_a, double coeff_a, double available_b, double coeff_b) {
    double extent_a = available_a / coeff_a;
    double extent_b = available_b / coeff_b;
    return extent_a < extent_b ? extent_a : extent_b;
}

double percent_yield(double actual, double theoretical) {
    return actual / theoretical * 100.0;
}

double dilution_volume(double c1, double c2, double v2) {
    return (c2 * v2) / c1;
}

int main(void) {
    double extent = limiting_extent(4.0, 2.0, 1.5, 1.0);
    double water_mol = extent * 2.0;
    double theoretical_yield = water_mol * 18.01528;

    printf("maximum_extent_mol=%.6f\n", extent);
    printf("water_mol_theoretical=%.6f\n", water_mol);
    printf("theoretical_yield_g=%.6f\n", theoretical_yield);
    printf("percent_yield=%.6f\n", percent_yield(45.0, theoretical_yield));
    printf("stock_volume_L=%.6f\n", dilution_volume(1.0, 0.1, 0.25));

    return 0;
}
