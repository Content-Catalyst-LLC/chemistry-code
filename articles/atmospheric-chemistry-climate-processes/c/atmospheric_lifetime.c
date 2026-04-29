#include <math.h>
#include <stdio.h>

/*
Atmospheric lifetime example.

C(t) = C0 * exp(-k t)
tau = 1 / k
t_half = ln(2) / k

Educational only. This model assumes first-order loss and no continuing source.
*/

double first_order_concentration(double c0, double k_per_day, double t_days) {
    return c0 * exp(-k_per_day * t_days);
}

int main(void) {
    double c0 = 100.0;
    double k = 0.20;
    double lifetime = 1.0 / k;
    double half_life = log(2.0) / k;

    printf("Atmospheric first-order lifetime example\n");
    printf("Initial mixing ratio: %.2f ppb\n", c0);
    printf("Loss rate: %.3f per day\n", k);
    printf("Lifetime: %.2f days\n", lifetime);
    printf("Half-life: %.2f days\n\n", half_life);

    printf("day,mixing_ratio_ppb,fraction_remaining\n");
    for (int day = 0; day <= 30; day += 5) {
        double c = first_order_concentration(c0, k, (double)day);
        printf("%d,%.5f,%.6f\n", day, c, c / c0);
    }

    return 0;
}
