#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Material {
    std::string material_id;
    std::string material_class;
    double band_gap_eV;
    double photostability_score;
    double processing_temperature_C;
    bool critical_material;
};

int main() {
    std::vector<Material> materials = {
        {"semi_A", "silicon", 1.12, 0.92, 950.0, false},
        {"semi_B", "metal_oxide", 3.20, 0.86, 450.0, false},
        {"semi_C", "organic_semiconductor", 1.85, 0.48, 120.0, false},
        {"semi_D", "hybrid_perovskite", 1.55, 0.58, 110.0, true},
        {"semi_E", "quantum_dot", 2.10, 0.42, 180.0, true}
    };

    std::cout << "C++ electronic material candidate classifier\n";

    for (const auto& material : materials) {
        bool useful_visible_gap = material.band_gap_eV >= 1.2 && material.band_gap_eV <= 2.3;
        bool stability_review = material.photostability_score < 0.60;
        bool processing_review = material.processing_temperature_C > 500.0;
        bool responsible_review = material.critical_material || stability_review || processing_review;

        if (useful_visible_gap || responsible_review) {
            std::cout << material.material_id
                      << " / " << material.material_class
                      << " visible_gap=" << useful_visible_gap
                      << ", stability_review=" << stability_review
                      << ", processing_review=" << processing_review
                      << ", responsible_review=" << responsible_review
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
