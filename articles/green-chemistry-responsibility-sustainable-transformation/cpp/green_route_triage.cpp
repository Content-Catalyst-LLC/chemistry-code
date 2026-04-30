/*
Green Chemistry, Responsibility, and Sustainable Transformation
C++ route triage and class aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Route {
    std::string route_name;
    std::string chemistry_class;
    double atom_economy;
    double waste_score;
    double pmi_score;
    double hazard_score;
    double solvent_score;
    double renewable;
    double circularity;
    double safety;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double greenScore(const Route& r) {
    return clamp01(
        0.15 * r.atom_economy +
        0.15 * r.waste_score +
        0.13 * r.pmi_score +
        0.14 * r.hazard_score +
        0.10 * r.solvent_score +
        0.10 * r.renewable +
        0.13 * r.circularity +
        0.10 * r.safety
    );
}

int main() {
    std::vector<Route> routes = {
        {"Route_A_Stoichiometric", "small_molecule_intermediate", 0.69, 0.44, 0.40, 0.45, 0.38, 0.20, 0.28, 0.42},
        {"Route_B_Catalytic", "small_molecule_intermediate", 0.80, 0.83, 0.75, 0.70, 0.65, 0.55, 0.60, 0.76},
        {"Route_C_Biocatalytic", "small_molecule_intermediate", 0.84, 0.87, 0.74, 0.78, 0.80, 0.70, 0.74, 0.73},
        {"Route_F_Flow_Chemistry", "specialty_chemical", 0.82, 0.88, 0.77, 0.74, 0.72, 0.40, 0.60, 0.87},
        {"Route_H_Circular_Material", "consumer_material", 0.82, 0.89, 0.79, 0.72, 0.70, 0.58, 0.77, 0.76}
    };

    std::map<std::string, double> sum_score;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_green_route_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_green_route_triage.csv");
    }

    out << "route_name,chemistry_class,green_score,profile_flag\n";

    for (const auto& route : routes) {
        double score = greenScore(route);
        std::string flag = score >= 0.70 ? "strong_green_design_profile" :
                           score >= 0.50 ? "moderate_profile_with_tradeoffs" :
                           "redesign_priority";

        out << route.route_name << ","
            << route.chemistry_class << ","
            << score << ","
            << flag << "\n";

        sum_score[route.chemistry_class] += score;
        counts[route.chemistry_class] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_green_route_class_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_green_route_class_summary.csv");
    }

    summary << "chemistry_class,n,mean_green_score\n";
    for (const auto& item : sum_score) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ green route triage complete.\n";
    return 0;
}
