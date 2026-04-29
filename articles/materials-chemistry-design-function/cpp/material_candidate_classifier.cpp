#include <iostream>
#include <string>
#include <vector>

struct Material {
    std::string material_id;
    std::string material_class;
    double density;
    double thermal_stability;
    double recyclability;
    double cost;
};

int main() {
    std::vector<Material> materials = {
        {"mat_A", "polymer_composite", 1.28, 180.0, 0.72, 0.35},
        {"mat_B", "ceramic", 3.85, 1150.0, 0.45, 0.62},
        {"mat_C", "porous_framework", 0.72, 320.0, 0.58, 0.80},
        {"mat_D", "alloy", 7.80, 780.0, 0.88, 0.55},
        {"mat_E", "semiconductor", 5.30, 540.0, 0.62, 0.90}
    };

    std::cout << "C++ materials candidate classifier\n";

    for (const auto& material : materials) {
        bool lightweight = material.density <= 1.5;
        bool thermally_stable = material.thermal_stability >= 300.0;
        bool responsible_design_candidate = material.recyclability >= 0.70 && material.cost <= 0.60;

        if (lightweight || thermally_stable || responsible_design_candidate) {
            std::cout << material.material_id
                      << " / " << material.material_class
                      << " flagged for review: "
                      << "lightweight=" << lightweight
                      << ", thermally_stable=" << thermally_stable
                      << ", responsible_design_candidate=" << responsible_design_candidate
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
