package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "run_manifest.csv")

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

	instruments := map[string]bool{}
	methods := map[string]bool{}
	statuses := map[string]bool{}

	for _, row := range rows[1:] {
		if len(row) != 11 {
			panic("malformed run manifest row")
		}
		instruments[row[3]] = true
		methods[row[4]] = true
		statuses[row[9]] = true
	}

	fmt.Println("Go laboratory automation CSV audit")
	fmt.Printf("Run rows: %d\n", len(rows)-1)
	fmt.Printf("Instrument count: %d\n", len(instruments))
	fmt.Printf("Method count: %d\n", len(methods))
	fmt.Printf("QC status count: %d\n", len(statuses))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
