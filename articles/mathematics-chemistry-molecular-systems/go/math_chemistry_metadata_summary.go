package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

// Portable summary helper for mathematical chemistry metadata.
func main() {
	files := []string{
		"stoichiometry_examples.csv",
		"ph_examples.csv",
		"kinetics_examples.csv",
		"thermodynamics_examples.csv",
		"molecular_coordinates.csv",
		"matrix_examples.csv",
		"uncertainty_components.csv",
		"molecular_graph_edges.csv",
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
