package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

// Portable summary helper for chemical metrology metadata.
func main() {
	files := []string{
		"uncertainty_budget.csv",
		"reference_materials.csv",
		"traceability_chain.csv",
		"interlaboratory_comparison.csv",
		"calibration_hierarchy.csv",
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
