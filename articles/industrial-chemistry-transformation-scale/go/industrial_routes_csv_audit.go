package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
)

func main() {
	dataPath := filepath.Join("..", "data", "process_routes.csv")

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

	processTypes := map[string]bool{}
	reviewCount := 0

	for _, row := range rows[1:] {
		if len(row) != 12 {
			panic("malformed process route row")
		}

		processTypes[row[1]] = true

		actual, _ := strconv.ParseFloat(row[3], 64)
		waste, _ := strconv.ParseFloat(row[4], 64)
		solvent, _ := strconv.ParseFloat(row[5], 64)
		hazard, _ := strconv.ParseFloat(row[9], 64)
		separation, _ := strconv.ParseFloat(row[10], 64)

		eFactor := waste / actual
		solventIntensity := solvent / actual

		if eFactor > 1.0 || solventIntensity > 2.0 || hazard > 0.60 || separation > 0.70 {
			reviewCount++
		}
	}

	fmt.Println("Go industrial routes CSV audit")
	fmt.Printf("Route rows: %d\n", len(rows)-1)
	fmt.Printf("Process type count: %d\n", len(processTypes))
	fmt.Printf("Review-like rows: %d\n", reviewCount)
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
