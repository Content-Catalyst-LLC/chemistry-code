#include <cmath>
#include <iomanip>
#include <iostream>

/*
Simplified methane oxidation lifetime calculation.

For a bimolecular reaction:
rate = k[OH][CH4]

If OH is treated as approximately constant for a teaching example,
the pseudo-first-order loss rate is:
k_prime = k[OH]

This example is conceptual and unit-sensitive. It is not a full atmospheric
chemistry mechanism.
*/

double pseudo_first_order_rate(double bimolecular_rate, double oh_concentration) {
    return bimolecular_rate * oh_concentration;
}

double lifetime_seconds(double k_prime) {
    return 1.0 / k_prime;
}

int main() {
    const double k_oh_ch4 = 6.3e-15;      // cm3 molecule-1 s-1, illustrative
    const double oh = 1.0e6;              // molecules cm-3, illustrative
    const double seconds_per_day = 86400.0;

    double k_prime = pseudo_first_order_rate(k_oh_ch4, oh);
    double tau_days = lifetime_seconds(k_prime) / seconds_per_day;

    std::cout << "Simplified methane oxidation lifetime example\n";
    std::cout << std::scientific << std::setprecision(3);
    std::cout << "k(OH + CH4): " << k_oh_ch4 << " cm3 molecule-1 s-1\n";
    std::cout << "[OH]: " << oh << " molecules cm-3\n";
    std::cout << "pseudo-first-order rate: " << k_prime << " s-1\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "lifetime: " << tau_days << " days\n";

    return 0;
}
