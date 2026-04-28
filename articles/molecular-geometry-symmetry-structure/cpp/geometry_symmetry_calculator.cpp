#include <array>
#include <cmath>
#include <iomanip>
#include <iostream>

double distance(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    double dx = a[0] - b[0];
    double dy = a[1] - b[1];
    double dz = a[2] - b[2];
    return std::sqrt(dx * dx + dy * dy + dz * dz);
}

double dot(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

std::array<double, 3> subtract(const std::array<double, 3>& a, const std::array<double, 3>& b) {
    return {a[0] - b[0], a[1] - b[1], a[2] - b[2]};
}

double angle_degrees(
    const std::array<double, 3>& a,
    const std::array<double, 3>& b,
    const std::array<double, 3>& c
) {
    auto u = subtract(a, b);
    auto v = subtract(c, b);

    double cos_theta = dot(u, v) / (std::sqrt(dot(u, u)) * std::sqrt(dot(v, v)));
    cos_theta = std::max(-1.0, std::min(1.0, cos_theta));

    return std::acos(cos_theta) * 180.0 / M_PI;
}

int main() {
    std::array<double, 3> oxygen {0.0, 0.0, 0.0};
    std::array<double, 3> h1 {0.958, 0.0, 0.0};
    std::array<double, 3> h2 {-0.239, 0.927, 0.0};

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "OH distance angstrom=" << distance(oxygen, h1) << "\n";
    std::cout << std::setprecision(3);
    std::cout << "HOH angle degrees=" << angle_degrees(h1, oxygen, h2) << "\n";

    return 0;
}
