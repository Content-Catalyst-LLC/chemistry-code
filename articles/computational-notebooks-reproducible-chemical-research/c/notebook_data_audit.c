#include <stdio.h>
#include <stdint.h>

int main(void) {
    const char *path = "../data/synthetic_chemical_notebook_runs.csv";
    FILE *file = fopen(path, "rb");

    if (!file) {
        perror("Could not open synthetic data file");
        return 1;
    }

    uint64_t checksum = 1469598103934665603ULL;
    uint64_t prime = 1099511628211ULL;
    unsigned long long byte_count = 0;
    unsigned long long line_count = 0;

    int c;
    while ((c = fgetc(file)) != EOF) {
        checksum ^= (unsigned char)c;
        checksum *= prime;
        byte_count++;
        if (c == '\n') {
            line_count++;
        }
    }

    fclose(file);

    printf("C data audit for synthetic chemical notebook records\n");
    printf("Bytes read: %llu\n", byte_count);
    printf("Lines read: %llu\n", line_count);
    printf("FNV-1a style checksum: %llu\n", (unsigned long long)checksum);
    printf("Responsible-use note: synthetic educational data only.\n");

    return 0;
}
