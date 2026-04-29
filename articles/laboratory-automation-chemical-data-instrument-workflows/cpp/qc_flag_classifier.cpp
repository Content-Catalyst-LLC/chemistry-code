#include <iostream>
#include <string>
#include <vector>

struct RunRecord {
    std::string run_id;
    std::string sample_id;
    std::string qc_status;
    double metadata_completeness;
    bool exception_flag;
};

int main() {
    std::vector<RunRecord> runs = {
        {"run_001", "blank", "pass", 1.00, false},
        {"run_002", "std_01", "pass", 1.00, false},
        {"run_003", "qc_01", "pass", 1.00, false},
        {"run_004", "sample_A", "pass", 1.00, false},
        {"run_005", "sample_B", "warning", 1.00, true},
        {"run_006", "sample_C", "failed", 0.60, true}
    };

    std::cout << "C++ automation QC flag classifier\n";

    for (const auto& run : runs) {
        bool review_required =
            run.qc_status != "pass" ||
            run.metadata_completeness < 1.0 ||
            run.exception_flag;

        if (review_required) {
            std::cout << run.run_id
                      << " / " << run.sample_id
                      << " requires review; QC status = "
                      << run.qc_status
                      << ", metadata completeness = "
                      << run.metadata_completeness
                      << "\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational review logic only.\n";
    return 0;
}
