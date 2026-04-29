#include <math.h>
#include <stdio.h>

int main(void) {
    double voltage = 3.2;
    double specificCapacity = 160.0;
    double activeMass = 12.0;

    double cellCapacity_mAh = specificCapacity * activeMass;
    double cellEnergy_Wh = cellCapacity_mAh * voltage / 1000.0;

    double dischargeCapacity = 1843.0;
    double chargeCapacity = 1847.0;
    double coulombicEfficiency = dischargeCapacity / chargeCapacity;

    double R = 8.314462618;
    double T = 298.15;
    double F = 96485.33212;
    double n = 1.0;
    double reactionQuotient = 0.1;
    double standardPotential = 3.4;
    double potential = standardPotential - (R * T / (n * F)) * log(reactionQuotient);

    printf("Electrochemistry metric utility\n");
    printf("Cell capacity mAh: %.6f\n", cellCapacity_mAh);
    printf("Cell energy Wh: %.6f\n", cellEnergy_Wh);
    printf("Coulombic efficiency: %.8f\n", coulombicEfficiency);
    printf("Nernst-style potential V: %.8f\n", potential);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
