#include <cmath>
#include <iomanip>
#include <iostream>

double lennard_jones(double r_angstrom, double epsilon_kj_mol, double sigma_angstrom) {
    double ratio = sigma_angstrom / r_angstrom;
    return 4.0 * epsilon_kj_mol * (std::pow(ratio, 12.0) - std::pow(ratio, 6.0));
}

double coulomb_relative(double q1, double q2, double r) {
    return q1 * q2 / r;
}

int main() {
    double epsilon = 0.997;
    double sigma = 3.40;
    double r_min = std::pow(2.0, 1.0 / 6.0) * sigma;
    double u_min = lennard_jones(r_min, epsilon, sigma);

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "r_min_angstrom=" << r_min << "\n";
    std::cout << "u_min_kj_mol=" << u_min << "\n";
    std::cout << "relative_coulomb_attraction=" << coulomb_relative(1.0, -1.0, 2.0) << "\n";

    return 0;
}
