#include <math.h>
#include <stdio.h>

/*
Environmental chemistry mass-balance example.

C(t) = C0 * exp(-k * t)

This educational model assumes a well-mixed compartment, first-order loss,
and no continuing source after the pulse release.
*/

double first_order_concentration(double c0, double k, double t_days) {
    return c0 * exp(-k * t_days);
}

int main(void) {
    double c0 = 100.0;
    double k = 0.08;
    double half_life = log(2.0) / k;

    printf("First-order environmental decay model\n");
    printf("Initial concentration: %.2f ug/L\n", c0);
    printf("Rate constant: %.4f per day\n", k);
    printf("Half-life: %.2f days\n\n", half_life);

    printf("day,concentration_ug_L,fraction_remaining\n");
    for (int day = 0; day <= 60; day += 10) {
        double c = first_order_concentration(c0, k, (double)day);
        printf("%d,%.4f,%.6f\n", day, c, c / c0);
    }

    return 0;
}
