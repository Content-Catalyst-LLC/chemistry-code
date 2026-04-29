#include <math.h>
#include <stdio.h>

double clamp_nonnegative(double value) {
    return value < 0.0 ? 0.0 : value;
}

int main(void) {
    double a = 1.0;
    double b = 0.0;
    double c = 0.0;
    double d = 0.0;
    double e = 0.0;

    double k1 = 0.20;
    double k2 = 0.08;
    double k3 = 0.05;
    double k4 = 0.03;
    double dt = 0.25;
    double total_time = 50.0;

    for (double t = 0.0; t <= total_time; t += dt) {
        double r1 = k1 * a;
        double r2 = k2 * b;
        double r3 = k3 * a;
        double r4 = k4 * b;

        a = clamp_nonnegative(a + (-r1 - r3) * dt);
        b = clamp_nonnegative(b + (r1 - r2 - r4) * dt);
        c = clamp_nonnegative(c + r2 * dt);
        d = clamp_nonnegative(d + r3 * dt);
        e = clamp_nonnegative(e + r4 * dt);
    }

    printf("A_final=%.6f\n", a);
    printf("B_final=%.6f\n", b);
    printf("C_final=%.6f\n", c);
    printf("D_final=%.6f\n", d);
    printf("E_final=%.6f\n", e);

    return 0;
}
