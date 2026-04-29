package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "colloid_systems.csv")

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

	systemTypes := map[string]bool{}
	continuousPhases := map[string]bool{}

	for _, row := range rows[1:] {
		if len(row) != 11 {
			panic("malformed colloid systems row")
		}
		systemTypes[row[1]] = true
		continuousPhases[row[3]] = true
	}

	fmt.Println("Go colloid CSV audit")
	fmt.Printf("System rows: %d\n", len(rows)-1)
	fmt.Printf("System type count: %d\n", len(systemTypes))
	fmt.Printf("Continuous phase count: %d\n", len(continuousPhases))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
