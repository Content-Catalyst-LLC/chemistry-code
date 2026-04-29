#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Nanoparticle {
    std::string sample_id;
    std::string material_class;
    double core_diameter_nm;
    double hydrodynamic_diameter_nm;
    double zeta_potential_mV;
    double polydispersity_index;
    double aggregation_after_salt_relative;
    bool critical_material;
};

int main() {
    std::vector<Nanoparticle> particles = {
        {"nano_A", "gold", 18.0, 24.0, -34.0, 0.08, 0.05, false},
        {"nano_B", "silica", 55.0, 72.0, -18.0, 0.18, 0.18, false},
        {"nano_C", "iron_oxide", 32.0, 48.0, 22.0, 0.22, 0.31, false},
        {"nano_D", "quantum_dot", 6.0, 12.0, -28.0, 0.11, 0.12, true},
        {"nano_E", "polymer_nanoparticle", 95.0, 140.0, -9.0, 0.34, 0.62, false}
    };

    std::cout << "C++ nanoparticle candidate classifier\n";

    for (const auto& particle : particles) {
        bool nanoscale_core = particle.core_diameter_nm >= 1.0 && particle.core_diameter_nm <= 100.0;
        bool colloidal_review =
            particle.polydispersity_index > 0.25 ||
            particle.aggregation_after_salt_relative > 0.30 ||
            std::abs(particle.zeta_potential_mV) < 15.0;
        bool responsible_review = particle.critical_material || colloidal_review;

        if (nanoscale_core || responsible_review) {
            std::cout << particle.sample_id
                      << " / " << particle.material_class
                      << " nanoscale_core=" << nanoscale_core
                      << ", colloidal_review=" << colloidal_review
                      << ", responsible_review=" << responsible_review
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
