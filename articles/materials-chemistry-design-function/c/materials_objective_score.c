#include <stdio.h>

int main(void) {
    double density = 1.28;
    double modulus = 4.2;
    double thermal = 180.0;
    double recycle = 0.72;
    double cost = 0.35;

    double score =
        1.2 * ((density - 1.5) / 1.0) * ((density - 1.5) / 1.0) +
        0.8 * ((modulus - 10.0) / 25.0) * ((modulus - 10.0) / 25.0) +
        1.0 * ((thermal - 300.0) / 250.0) * ((thermal - 300.0) / 250.0) +
        1.4 * ((recycle - 0.85) / 0.25) * ((recycle - 0.85) / 0.25) +
        1.2 * ((cost - 0.30) / 0.30) * ((cost - 0.30) / 0.30);

    printf("Materials objective-score utility\n");
    printf("Synthetic objective score: %.8f\n", score);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
