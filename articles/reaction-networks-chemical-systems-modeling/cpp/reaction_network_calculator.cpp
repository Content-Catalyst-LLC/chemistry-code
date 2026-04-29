#include <algorithm>
#include <iomanip>
#include <iostream>

int main() {
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

        a = std::max(a + (-r1 - r3) * dt, 0.0);
        b = std::max(b + (r1 - r2 - r4) * dt, 0.0);
        c = std::max(c + r2 * dt, 0.0);
        d = std::max(d + r3 * dt, 0.0);
        e = std::max(e + r4 * dt, 0.0);
    }

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "A_final=" << a << "\n";
    std::cout << "B_final=" << b << "\n";
    std::cout << "C_final=" << c << "\n";
    std::cout << "D_final=" << d << "\n";
    std::cout << "E_final=" << e << "\n";

    return 0;
}
