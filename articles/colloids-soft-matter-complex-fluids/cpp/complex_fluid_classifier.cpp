#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct ComplexFluid {
    std::string formulation_id;
    std::string system_type;
    double zeta_potential_mV;
    double volume_fraction;
    double low_shear_viscosity;
    double high_shear_viscosity;
    double yield_stress;
    double salt_aggregation_index;
};

int main() {
    std::vector<ComplexFluid> systems = {
        {"col_A", "silica_sol", -42.0, 0.04, 0.012, 0.010, 0.0, 0.08},
        {"col_B", "oil_in_water_emulsion", -18.0, 0.22, 0.85, 0.19, 4.2, 0.22},
        {"col_C", "particle_gel", -12.0, 0.35, 18.0, 1.2, 85.0, 0.48},
        {"col_D", "surfactant_micelles", -5.0, 0.02, 0.006, 0.005, 0.0, 0.05},
        {"col_E", "clay_suspension", -35.0, 0.28, 5.4, 0.82, 36.0, 0.31}
    };

    std::cout << "C++ complex fluid classifier\n";

    for (const auto& system : systems) {
        bool electrostatic_review = std::abs(system.zeta_potential_mV) < 20.0;
        bool aggregation_review = system.salt_aggregation_index > 0.30;
        bool yield_stress_review = system.yield_stress > 10.0;
        bool shear_thinning = (system.low_shear_viscosity / system.high_shear_viscosity) > 5.0;

        if (electrostatic_review || aggregation_review || yield_stress_review || shear_thinning) {
            std::cout << system.formulation_id
                      << " / " << system.system_type
                      << " flagged: electrostatic_review=" << electrostatic_review
                      << ", aggregation_review=" << aggregation_review
                      << ", yield_stress_review=" << yield_stress_review
                      << ", shear_thinning=" << shear_thinning
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
