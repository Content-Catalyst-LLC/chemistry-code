package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

// Portable summary helper for Chemical Revolution examples.
func main() {
	files := []string{
		"mass_conservation_examples.csv",
		"oxidation_mass_gain.csv",
		"combustion_stoichiometry.csv",
		"nomenclature_mapping.csv",
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
