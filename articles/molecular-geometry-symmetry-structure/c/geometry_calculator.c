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

double dot_3d(double a[3], double b[3]) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

double angle_degrees(double a[3], double b[3], double c[3]) {
    double u[3] = {a[0] - b[0], a[1] - b[1], a[2] - b[2]};
    double v[3] = {c[0] - b[0], c[1] - b[1], c[2] - b[2]};

    double cos_theta = dot_3d(u, v) / sqrt(dot_3d(u, u) * dot_3d(v, v));

    if (cos_theta > 1.0) cos_theta = 1.0;
    if (cos_theta < -1.0) cos_theta = -1.0;

    return acos(cos_theta) * 180.0 / M_PI;
}

int main(void) {
    double oxygen[3] = {0.0, 0.0, 0.0};
    double h1[3] = {0.958, 0.0, 0.0};
    double h2[3] = {-0.239, 0.927, 0.0};

    printf("OH distance angstrom=%.6f\n", distance_3d(0.0, 0.0, 0.0, 0.958, 0.0, 0.0));
    printf("HOH angle degrees=%.3f\n", angle_degrees(h1, oxygen, h2));

    return 0;
}
