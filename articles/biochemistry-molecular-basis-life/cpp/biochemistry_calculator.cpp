#include <cmath>
#include <iomanip>
#include <iostream>

double michaelis_menten(double substrate, double vmax, double km) {
    return vmax * substrate / (km + substrate);
}

double occupancy(double ligand, double kd) {
    return ligand / (kd + ligand);
}

double hill_occupancy(double ligand, double kd, double n) {
    return std::pow(ligand, n) / (std::pow(kd, n) + std::pow(ligand, n));
}

double delta_g_standard(double k, double temperature_k) {
    constexpr double R = 8.314462618;
    return -(R * temperature_k * std::log(k)) / 1000.0;
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "velocity=" << michaelis_menten(5.0, 120.0, 3.5) << "\n";
    std::cout << "occupancy=" << occupancy(2.0, 2.0) << "\n";
    std::cout << "hill_occupancy=" << hill_occupancy(2.0, 2.0, 2.0) << "\n";
    std::cout << "delta_g_kj_mol=" << delta_g_standard(1000.0, 298.15) << "\n";
    return 0;
}
