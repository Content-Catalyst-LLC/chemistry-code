package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "ms_features.csv")

	file, err := os.Open(dataPath)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	rows, err := reader.ReadAll()
	if err != nil {
		panic(err)
	}

	if len(rows) < 2 {
		panic("expected header and at least one data row")
	}

	samples := map[string]bool{}
	ionModes := map[string]bool{}
	adducts := map[string]bool{}

	for _, row := range rows[1:] {
		if len(row) != 8 {
			panic("malformed MS feature row")
		}
		samples[row[1]] = true
		ionModes[row[6]] = true
		adducts[row[7]] = true
	}

	fmt.Println("Go mass spectrometry CSV audit")
	fmt.Printf("Feature rows: %d\n", len(rows)-1)
	fmt.Printf("Sample count: %d\n", len(samples))
	fmt.Printf("Ion mode count: %d\n", len(ionModes))
	fmt.Printf("Adduct count: %d\n", len(adducts))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
