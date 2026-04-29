#include <iostream>
#include <string>
#include <vector>

std::string classify_region(double wavenumber) {
    if (wavenumber >= 3200 && wavenumber <= 3600) {
        return "possible O-H or N-H stretching region";
    }
    if (wavenumber >= 3000 && wavenumber <= 3100) {
        return "possible aromatic or alkene C-H stretching region";
    }
    if (wavenumber >= 2850 && wavenumber < 3000) {
        return "possible aliphatic C-H stretching region";
    }
    if (wavenumber >= 1650 && wavenumber <= 1800) {
        return "possible carbonyl stretching region";
    }
    if (wavenumber >= 1500 && wavenumber < 1650) {
        return "possible C=C or aromatic ring region";
    }
    if (wavenumber >= 1000 && wavenumber <= 1300) {
        return "possible C-O, C-N, or fingerprint-region feature";
    }
    if (wavenumber >= 650 && wavenumber <= 900) {
        return "possible aromatic C-H out-of-plane region";
    }
    return "unassigned educational region";
}

int main() {
    std::vector<double> peaks = {3350, 3060, 2960, 1718, 1602, 1250, 755};

    std::cout << "C++ educational IR functional-region classifier\n";

    for (double peak : peaks) {
        std::cout << peak << " cm^-1: " << classify_region(peak) << "\n";
    }

    std::cout << "Responsible-use note: synthetic educational interpretation only.\n";
    return 0;
}
