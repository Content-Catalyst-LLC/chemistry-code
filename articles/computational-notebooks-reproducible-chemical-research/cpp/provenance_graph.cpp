#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> fields;
    std::stringstream stream(line);
    std::string field;

    while (std::getline(stream, field, ',')) {
        fields.push_back(field);
    }

    return fields;
}

int main() {
    const std::string path = "../data/synthetic_chemical_notebook_runs.csv";
    std::ifstream file(path);

    if (!file) {
        std::cerr << "Could not open " << path << "\n";
        return 1;
    }

    std::string line;
    std::getline(file, line);

    std::map<std::string, std::set<std::string>> provenance_edges;

    while (std::getline(file, line)) {
        auto fields = split_csv_line(line);

        if (fields.size() != 12) {
            std::cerr << "Malformed row: " << line << "\n";
            return 1;
        }

        const std::string notebook = fields[1];
        const std::string instrument = "instrument:" + fields[4];
        const std::string environment = "environment:" + fields[5];
        const std::string molecule = "molecule:" + fields[2];
        const std::string analyst = "analyst:" + fields[9];

        provenance_edges[notebook].insert(instrument);
        provenance_edges[notebook].insert(environment);
        provenance_edges[notebook].insert(molecule);
        provenance_edges[notebook].insert(analyst);
    }

    std::cout << "C++ provenance graph for synthetic chemical notebooks\n";

    for (const auto& entry : provenance_edges) {
        std::cout << entry.first << " -> ";
        bool first = true;

        for (const auto& node : entry.second) {
            if (!first) {
                std::cout << ", ";
            }

            std::cout << node;
            first = false;
        }

        std::cout << "\n";
    }

    std::cout << "Responsible-use note: synthetic educational data only.\n";
    return 0;
}
