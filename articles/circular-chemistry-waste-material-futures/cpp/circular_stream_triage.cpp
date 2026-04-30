/*
Circular Chemistry, Waste, and Material Futures
C++ material-stream triage and class aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Stream {
    std::string stream_name;
    std::string material_class;
    std::string pathway;
    double recovery;
    double retention;
    double infrastructure;
    double safety;
    double energy_score;
    double traceability;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double circularScore(const Stream& s) {
    return clamp01(
        0.20 * s.recovery +
        0.22 * s.retention +
        0.16 * s.infrastructure +
        0.18 * s.safety +
        0.10 * s.energy_score +
        0.14 * s.traceability
    );
}

int main() {
    std::vector<Stream> streams = {
        {"PET_bottles_clear", "polymer", "mechanical_recycling", 0.76, 0.45, 0.72, 0.82, 0.88, 0.78},
        {"Multilayer_film", "polymer", "chemical_recycling", 0.42, 0.11, 0.37, 0.58, 0.26, 0.35},
        {"Aluminum_scrap", "metal", "remelting", 0.90, 0.78, 0.82, 0.86, 0.86, 0.82},
        {"Lithium_ion_batteries", "battery", "hydrometallurgical_recovery", 0.62, 0.35, 0.60, 0.48, 0.16, 0.70},
        {"Solvent_wash_stream", "solvent", "distillation_recovery", 0.84, 0.64, 0.84, 0.62, 0.87, 0.75}
    };

    std::map<std::string, double> sum_score;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_circular_stream_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_circular_stream_triage.csv");
    }

    out << "stream_name,material_class,pathway,circular_score,profile_flag\n";

    for (const auto& stream : streams) {
        double score = circularScore(stream);
        std::string flag = score >= 0.70 ? "strong_circular_profile" :
                           score >= 0.50 ? "moderate_profile_with_constraints" :
                           "redesign_or_infrastructure_priority";

        out << stream.stream_name << ","
            << stream.material_class << ","
            << stream.pathway << ","
            << score << ","
            << flag << "\n";

        sum_score[stream.material_class] += score;
        counts[stream.material_class] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_circular_material_class_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_circular_material_class_summary.csv");
    }

    summary << "material_class,n,mean_circular_score\n";
    for (const auto& item : sum_score) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ circular stream triage complete.\n";
    return 0;
}
