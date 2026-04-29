#include <iostream>
#include <string>
#include <vector>

struct Catalyst {
    std::string catalyst_id;
    std::string catalyst_class;
    double surface_area;
    double selectivity;
    bool critical_metal;
};

int main() {
    std::vector<Catalyst> catalysts = {
        {"cat_A", "supported_metal", 85.0, 0.82, false},
        {"cat_B", "acidic_oxide", 210.0, 0.74, false},
        {"cat_C", "metal_oxide_interface", 145.0, 0.88, true},
        {"cat_D", "porous_carbon", 60.0, 0.61, false},
        {"cat_E", "zeolite", 430.0, 0.91, false},
        {"cat_F", "single_atom_catalyst", 75.0, 0.86, true}
    };

    std::cout << "C++ catalyst candidate classifier\n";

    for (const auto& catalyst : catalysts) {
        bool high_surface_area = catalyst.surface_area >= 200.0;
        bool high_selectivity = catalyst.selectivity >= 0.85;
        bool review_required = catalyst.critical_metal;

        if (high_surface_area || high_selectivity || review_required) {
            std::cout << catalyst.catalyst_id
                      << " / " << catalyst.catalyst_class
                      << " flagged: high_surface_area=" << high_surface_area
                      << ", high_selectivity=" << high_selectivity
                      << ", critical_material_review=" << review_required
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
