package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "chromatographic_peaks.csv")

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
	detectors := map[string]bool{}

	for _, row := range rows[1:] {
		if len(row) != 6 {
			panic("malformed chromatographic peak row")
		}
		samples[row[1]] = true
		detectors[row[5]] = true
	}

	fmt.Println("Go chromatography CSV audit")
	fmt.Printf("Peak rows: %d\n", len(rows)-1)
	fmt.Printf("Sample count: %d\n", len(samples))
	fmt.Printf("Detector count: %d\n", len(detectors))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
