/*
Chemistry, Classification, and the Human Understanding of Matter
C++ chemical class triage and aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct ChemicalRecord {
    std::string sample_name;
    std::string assigned_class;
    double evidence_score;
    double classification_reliability;
    double hazard_indicator_score;
    double qc_score;
};

int main() {
    std::vector<ChemicalRecord> records = {
        {"ethyl_acetate_reference", "organic_molecular_substance", 0.86, 0.88, 0.22, 0.94},
        {"seawater_sample", "mixture_or_solution", 0.70, 0.75, 0.35, 0.90},
        {"sodium_chloride_crystal", "ionic_or_salt_crystal", 0.86, 0.90, 0.18, 0.96},
        {"polyethylene_film", "polymer_material", 0.78, 0.82, 0.20, 0.92},
        {"soil_extract", "heterogeneous_mixture", 0.60, 0.62, 0.62, 0.82}
    };

    std::map<std::string, double> reliability_sum;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_chemical_class_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_chemical_class_triage.csv");
    }

    out << "sample_name,assigned_class,classification_reliability,hazard_attention\n";

    for (const auto& record : records) {
        std::string hazard = record.hazard_indicator_score >= 0.60 ? "higher_attention" :
                             record.hazard_indicator_score >= 0.35 ? "moderate_attention" :
                             "lower_attention";

        out << record.sample_name << ","
            << record.assigned_class << ","
            << record.classification_reliability << ","
            << hazard << "\n";

        reliability_sum[record.assigned_class] += record.classification_reliability;
        counts[record.assigned_class] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_chemical_class_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_chemical_class_summary.csv");
    }

    summary << "assigned_class,n,mean_classification_reliability\n";
    for (const auto& item : reliability_sum) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ chemical class triage complete.\n";
    return 0;
}
