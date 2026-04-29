#include <iostream>
#include <string>
#include <vector>

struct Polymer {
    std::string polymer_id;
    std::string polymer_class;
    double oxygen_permeability;
    double modulus;
    double elongation;
    double recyclability;
    double cost;
};

int main() {
    std::vector<Polymer> polymers = {
        {"poly_A", "polyolefin", 0.80, 900, 450, 0.82, 0.28},
        {"poly_B", "polyester", 0.18, 2400, 120, 0.74, 0.42},
        {"poly_C", "polyamide", 0.12, 1800, 180, 0.52, 0.55},
        {"poly_D", "elastomer", 2.80, 4, 700, 0.35, 0.38},
        {"poly_E", "biopolymer", 0.35, 3200, 40, 0.68, 0.62}
    };

    std::cout << "C++ polymer candidate classifier\n";

    for (const auto& polymer : polymers) {
        bool barrier_candidate = polymer.oxygen_permeability <= 0.25;
        bool flexible_candidate = polymer.elongation >= 300.0;
        bool responsible_design_candidate = polymer.recyclability >= 0.70 && polymer.cost <= 0.50;

        if (barrier_candidate || flexible_candidate || responsible_design_candidate) {
            std::cout << polymer.polymer_id
                      << " / " << polymer.polymer_class
                      << " flagged for review: "
                      << "barrier=" << barrier_candidate
                      << ", flexible=" << flexible_candidate
                      << ", responsible_design_candidate=" << responsible_design_candidate
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
