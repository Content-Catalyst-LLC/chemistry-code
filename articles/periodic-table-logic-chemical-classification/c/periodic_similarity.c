#include <stdio.h>
#include <math.h>

double isotope_weighted_mass(
    double mass_a,
    double abundance_a,
    double mass_b,
    double abundance_b
) {
    return mass_a * abundance_a + mass_b * abundance_b;
}

int neutron_number(int mass_number, int atomic_number) {
    return mass_number - atomic_number;
}

double feature_distance_4d(double a[4], double b[4]) {
    double total = 0.0;
    for (int i = 0; i < 4; i++) {
        double delta = a[i] - b[i];
        total += delta * delta;
    }
    return sqrt(total);
}

int main(void) {
    double chlorine_mass = isotope_weighted_mass(
        34.96885268,
        0.7576,
        36.96590260,
        0.2424
    );

    double li[4] = {1.0, 2.0, 128.0, 520.0};
    double na[4] = {1.0, 3.0, 166.0, 496.0};

    printf("chlorine_weighted_atomic_mass_u=%.6f\n", chlorine_mass);
    printf("carbon_13_neutron_number=%d\n", neutron_number(13, 6));
    printf("li_na_feature_distance_unscaled=%.6f\n", feature_distance_4d(li, na));

    return 0;
}
