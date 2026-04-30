/*
Environmental Chemistry and the Chemical Conditions of Habitability
C++ compartment-level screening and source-pathway-receptor logic.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Record {
    std::string site;
    std::string compartment;
    std::string analyte_class;
    double benchmark_ratio;
    double mobility_factor;
    double persistence_factor;
    double exposure_weight;
    double receptor_sensitivity;
    double nutrient_pressure;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double pressureIndex(const Record& r) {
    return clamp01(
        0.28 * clamp01(std::log1p(r.benchmark_ratio) / std::log(5.0)) +
        0.16 * r.mobility_factor +
        0.16 * r.persistence_factor +
        0.16 * r.exposure_weight +
        0.12 * r.receptor_sensitivity +
        0.12 * r.nutrient_pressure
    );
}

int main() {
    std::vector<Record> records = {
        {"Groundwater-B", "groundwater", "metalloid", 1.35, 0.80, 0.999, 0.95, 0.90, 0.10},
        {"Sediment-D", "sediment", "pah", 1.90, 0.02, 0.71, 0.55, 0.82, 0.25},
        {"Stormwater-F", "stormwater", "metal", 1.33, 0.45, 0.47, 0.72, 0.78, 0.90},
        {"Wetland-G", "wetland_water", "nutrient", 2.10, 0.55, 0.33, 0.62, 0.80, 0.92},
        {"Groundwater-I", "groundwater", "chlorinated_solvent", 1.70, 0.83, 0.80, 0.93, 0.91, 0.05}
    };

    std::map<std::string, double> sum_pressure;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_environmental_compartment_screening.csv");
    if (!out) {
        out.open("outputs/tables/cpp_environmental_compartment_screening.csv");
    }

    out << "site,compartment,analyte_class,pressure_index,attention_flag\n";

    for (const auto& record : records) {
        double pressure = pressureIndex(record);
        std::string flag = pressure >= 0.65 ? "high_attention" :
                           pressure >= 0.45 ? "moderate_attention" :
                           "monitor";

        out << record.site << ","
            << record.compartment << ","
            << record.analyte_class << ","
            << pressure << ","
            << flag << "\n";

        sum_pressure[record.compartment] += pressure;
        counts[record.compartment] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_environmental_compartment_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_environmental_compartment_summary.csv");
    }

    summary << "compartment,mean_pressure_index\n";
    for (const auto& item : sum_pressure) {
        summary << item.first << "," << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ environmental compartment screening complete.\n";
    return 0;
}
