#include <iomanip>
#include <iostream>

double dbe(double c, double h, double n, double x) {
    return c - (h + x) / 2.0 + n / 2.0 + 1.0;
}

double polarity_score(double heteroatoms, double donors, double acceptors) {
    return heteroatoms + donors + acceptors;
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "benzene_DBE=" << dbe(6.0, 6.0, 0.0, 0.0) << "\n";
    std::cout << "acetic_acid_DBE=" << dbe(2.0, 4.0, 0.0, 0.0) << "\n";
    std::cout << "polarity_score=" << polarity_score(2.0, 1.0, 2.0) << "\n";
    return 0;
}
