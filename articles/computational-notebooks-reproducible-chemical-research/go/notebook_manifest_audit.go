package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	baseDir := filepath.Join("..")
	dataPath := filepath.Join(baseDir, "data", "synthetic_chemical_notebook_runs.csv")

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

	notebooks := map[string]bool{}
	environments := map[string]bool{}
	instruments := map[string]bool{}

	for _, row := range rows[1:] {
		if len(row) != 12 {
			panic("malformed CSV row")
		}
		notebooks[row[1]] = true
		environments[row[5]] = true
		instruments[row[4]] = true
	}

	fmt.Println("Go notebook manifest audit")
	fmt.Printf("Rows: %d\n", len(rows)-1)
	fmt.Printf("Notebook count: %d\n", len(notebooks))
	fmt.Printf("Environment count: %d\n", len(environments))
	fmt.Printf("Instrument count: %d\n", len(instruments))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
