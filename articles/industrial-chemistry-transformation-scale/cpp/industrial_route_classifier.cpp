#include <iostream>
#include <string>
#include <vector>

struct Route {
    std::string route_id;
    std::string process_type;
    double yield_fraction;
    double e_factor;
    double solvent_intensity;
    double energy_intensity;
    double hazard_score;
    double separation_score;
};

int main() {
    std::vector<Route> routes = {
        {"ind_A", "batch_specialty", 0.82, 0.512, 1.829, 2.683, 0.42, 0.50},
        {"ind_B", "continuous_catalytic", 0.91, 0.231, 0.385, 1.758, 0.35, 0.32},
        {"ind_C", "solvent_heavy_batch", 0.76, 2.368, 5.526, 4.737, 0.68, 0.82},
        {"ind_D", "flow_intensified", 0.88, 0.295, 0.682, 1.591, 0.38, 0.36},
        {"ind_E", "biobased_route", 0.79, 0.658, 1.392, 2.405, 0.31, 0.55}
    };

    std::cout << "C++ industrial route classifier\n";

    for (const auto& route : routes) {
        bool waste_review = route.e_factor > 1.0;
        bool solvent_review = route.solvent_intensity > 2.0;
        bool energy_review = route.energy_intensity > 3.0;
        bool hazard_review = route.hazard_score > 0.60;
        bool separation_review = route.separation_score > 0.70;

        if (waste_review || solvent_review || energy_review || hazard_review || separation_review) {
            std::cout << route.route_id
                      << " / " << route.process_type
                      << " waste_review=" << waste_review
                      << ", solvent_review=" << solvent_review
                      << ", energy_review=" << energy_review
                      << ", hazard_review=" << hazard_review
                      << ", separation_review=" << separation_review
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational screening only.\n";
    return 0;
}
