#include <stdio.h>
#include <math.h>

#define AVOGADRO_CONSTANT 6.02214076e23

int neutron_number(int mass_number, int atomic_number) {
    return mass_number - atomic_number;
}

double isotope_weighted_mass(
    double mass_a,
    double abundance_a,
    double mass_b,
    double abundance_b
) {
    return mass_a * abundance_a + mass_b * abundance_b;
}

int main(void) {
    double chlorine_mass = isotope_weighted_mass(
        34.96885268,
        0.7576,
        36.96590260,
        0.2424
    );

    printf("chlorine_weighted_atomic_mass_u=%.6f\n", chlorine_mass);
    printf("carbon_14_neutron_number=%d\n", neutron_number(14, 6));
    printf("one_mole_entities=%.6e\n", AVOGADRO_CONSTANT);

    return 0;
}
