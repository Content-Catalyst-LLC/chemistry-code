package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

// Portable summary helper for measurement metadata.
func main() {
	files := []string{
		"mass_volume_concentration.csv",
		"calibration_curve.csv",
		"unknown_samples.csv",
		"replicate_measurements.csv",
		"dilution_plan.csv",
		"measurement_metadata.csv",
	}

	for _, name := range files {
		path := filepath.Join("data", name)
		file, err := os.Open(path)
		if err != nil {
			panic(err)
		}

		reader := csv.NewReader(file)
		records, err := reader.ReadAll()
		file.Close()

		if err != nil {
			panic(err)
		}

		fmt.Printf("%s rows=%d\n", name, len(records)-1)
	}
}
