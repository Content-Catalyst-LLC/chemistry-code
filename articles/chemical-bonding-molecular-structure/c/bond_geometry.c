#include <stdio.h>
#include <math.h>

double distance_3d(
    double ax, double ay, double az,
    double bx, double by, double bz
) {
    double dx = ax - bx;
    double dy = ay - by;
    double dz = az - bz;
    return sqrt(dx * dx + dy * dy + dz * dz);
}

double bond_order(double bonding_electrons, double antibonding_electrons) {
    return (bonding_electrons - antibonding_electrons) / 2.0;
}

int main(void) {
    double oh_distance = distance_3d(0.0, 0.0, 0.0, 0.958, 0.0, 0.0);
    double h2_bond_order = bond_order(2.0, 0.0);

    printf("oh_distance_angstrom=%.6f\n", oh_distance);
    printf("h2_bond_order=%.6f\n", h2_bond_order);

    return 0;
}
