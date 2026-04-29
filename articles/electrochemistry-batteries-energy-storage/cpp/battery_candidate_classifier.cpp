#include <iostream>
#include <string>
#include <vector>

struct Cell {
    std::string cell_id;
    std::string chemistry;
    double voltage;
    double specific_capacity;
    double active_mass;
    double retention;
    double coulombic_efficiency;
    double critical_material_score;
    double safety_review_score;
};

int main() {
    std::vector<Cell> cells = {
        {"bat_A", "lithium_iron_phosphate", 3.2, 160.0, 12.0, 0.96, 0.998, 0.22, 0.20},
        {"bat_B", "nickel_manganese_cobalt", 3.7, 190.0, 10.5, 0.91, 0.995, 0.78, 0.42},
        {"bat_C", "sodium_ion", 3.0, 125.0, 14.0, 0.94, 0.997, 0.30, 0.25},
        {"bat_D", "solid_state_lithium", 3.8, 220.0, 9.0, 0.86, 0.990, 0.65, 0.55},
        {"bat_E", "supercapacitor", 2.7, 40.0, 20.0, 0.99, 0.999, 0.18, 0.12}
    };

    std::cout << "C++ battery candidate classifier\n";

    for (const auto& cell : cells) {
        double cell_capacity_mAh = cell.specific_capacity * cell.active_mass;
        double cell_energy_Wh = cell_capacity_mAh * cell.voltage / 1000.0;

        bool degradation_review = cell.retention < 0.90;
        bool efficiency_review = cell.coulombic_efficiency < 0.995;
        bool critical_review = cell.critical_material_score > 0.60;
        bool safety_review = cell.safety_review_score > 0.40;

        if (degradation_review || efficiency_review || critical_review || safety_review) {
            std::cout << cell.cell_id
                      << " / " << cell.chemistry
                      << " energy_Wh=" << cell_energy_Wh
                      << ", degradation_review=" << degradation_review
                      << ", efficiency_review=" << efficiency_review
                      << ", critical_review=" << critical_review
                      << ", safety_review=" << safety_review
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
