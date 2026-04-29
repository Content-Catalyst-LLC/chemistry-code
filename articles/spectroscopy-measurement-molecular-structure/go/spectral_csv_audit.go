package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "ir_peaks.csv")

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

	for _, row := range rows[1:] {
		if len(row) != 4 {
			panic("malformed IR peak row")
		}
		samples[row[1]] = true
	}

	fmt.Println("Go spectral CSV audit")
	fmt.Printf("IR peak rows: %d\n", len(rows)-1)
	fmt.Printf("Sample count: %d\n", len(samples))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
