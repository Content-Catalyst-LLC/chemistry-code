#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

/*
Simple spectral-line catalog matching example.

This is educational only. Professional line identification requires
rest-frequency uncertainty, source velocity, multiple transitions,
line intensities, excitation, optical depth, and blending analysis.
*/

struct CatalogLine {
    std::string species;
    double rest_frequency_ghz;
};

struct Observation {
    std::string source;
    double observed_frequency_ghz;
};

int main() {
    std::vector<CatalogLine> catalog = {
        {"CO", 115.271},
        {"CH3OH", 96.741},
        {"HCN", 88.632},
        {"N2H+", 93.174}
    };

    std::vector<Observation> observations = {
        {"Cloud-A", 115.269},
        {"HotCore-B", 96.738},
        {"Disk-C", 88.631}
    };

    const double tolerance_ghz = 0.005;

    std::cout << "source,observed_frequency_GHz,candidate_species,rest_frequency_GHz,frequency_offset_GHz\n";
    std::cout << std::fixed << std::setprecision(6);

    for (const auto& obs : observations) {
        for (const auto& line : catalog) {
            double offset = obs.observed_frequency_ghz - line.rest_frequency_ghz;
            if (std::abs(offset) <= tolerance_ghz) {
                std::cout << obs.source << ","
                          << obs.observed_frequency_ghz << ","
                          << line.species << ","
                          << line.rest_frequency_ghz << ","
                          << offset << "\n";
            }
        }
    }

    return 0;
}
