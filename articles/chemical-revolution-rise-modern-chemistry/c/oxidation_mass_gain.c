#include <stdio.h>

// Compact oxidation mass-gain kernel.

int main(void) {
    double metal_mass_g = 24.305;
    double oxygen_mass_g = 16.000;
    double oxide_mass_g = metal_mass_g + oxygen_mass_g;
    double oxygen_mass_fraction = oxygen_mass_g / oxide_mass_g;

    printf("oxide_mass_g=%.6f\n", oxide_mass_g);
    printf("oxygen_mass_fraction=%.6f\n", oxygen_mass_fraction);

    return 0;
}
