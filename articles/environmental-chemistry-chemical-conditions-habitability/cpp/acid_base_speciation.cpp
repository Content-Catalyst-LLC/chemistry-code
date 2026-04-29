#include <cmath>
#include <iomanip>
#include <iostream>

/*
Weak-acid speciation model for environmental chemistry.

For HA <-> H+ + A-

A-/HA = 10^(pH - pKa)
neutral fraction HA = 1 / (1 + 10^(pH - pKa))

This matters because neutral and ionized forms can differ in sorption,
membrane permeability, volatility, and environmental mobility.
*/

double weak_acid_neutral_fraction(double pH, double pKa) {
    return 1.0 / (1.0 + std::pow(10.0, pH - pKa));
}

int main() {
    const double pKa = 6.5;

    std::cout << "Weak-acid environmental speciation example\n";
    std::cout << "pKa = " << pKa << "\n\n";
    std::cout << "pH,neutral_fraction,ionized_fraction\n";

    for (double pH = 4.0; pH <= 9.0; pH += 1.0) {
        double neutral = weak_acid_neutral_fraction(pH, pKa);
        double ionized = 1.0 - neutral;

        std::cout << std::fixed << std::setprecision(3)
                  << pH << ","
                  << neutral << ","
                  << ionized << "\n";
    }

    return 0;
}
