package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "material_candidates.csv")

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

	for _, row := range rows[1:] {
		if len(row) != 8 {
			panic("malformed material candidate row")
		}
		classes[row[1]] = true
	}

	fmt.Println("Go materials CSV audit")
	fmt.Printf("Candidate rows: %d\n", len(rows)-1)
	fmt.Printf("Material class count: %d\n", len(classes))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
