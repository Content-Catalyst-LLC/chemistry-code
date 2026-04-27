#include <math.h>
#include <stdio.h>

// Compact stoichiometry and pH kernel.

int main(void) {
    double hydrogen_moles = 4.0;
    double oxygen_required = hydrogen_moles / 2.0;
    double water_produced = hydrogen_moles;

    double hydrogen_activity = 1.0e-5;
    double ph = -log10(hydrogen_activity);

    printf("oxygen_required_mol=%.6f\n", oxygen_required);
    printf("water_produced_mol=%.6f\n", water_produced);
    printf("pH=%.6f\n", ph);

    return 0;
}
