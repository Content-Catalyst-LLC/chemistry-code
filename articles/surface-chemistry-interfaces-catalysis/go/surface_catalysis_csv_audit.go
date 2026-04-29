package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "catalyst_candidates.csv")

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

	classes := map[string]bool{}
	criticalCount := 0

	for _, row := range rows[1:] {
		if len(row) != 9 {
			panic("malformed catalyst candidate row")
		}
		classes[row[1]] = true
		if row[8] == "true" {
			criticalCount++
		}
	}

	fmt.Println("Go surface catalysis CSV audit")
	fmt.Printf("Catalyst rows: %d\n", len(rows)-1)
	fmt.Printf("Catalyst class count: %d\n", len(classes))
	fmt.Printf("Critical material flagged rows: %d\n", criticalCount)
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
