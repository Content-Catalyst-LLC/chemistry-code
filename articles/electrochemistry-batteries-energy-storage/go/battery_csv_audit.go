package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
)

func main() {
	dataPath := filepath.Join("..", "data", "cell_candidates.csv")

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

	chemistries := map[string]bool{}
	reviewCount := 0

	for _, row := range rows[1:] {
		if len(row) != 10 {
			panic("malformed cell candidate row")
		}

		chemistries[row[1]] = true

		criticalScore, _ := strconv.ParseFloat(row[8], 64)
		safetyScore, _ := strconv.ParseFloat(row[9], 64)

		if criticalScore > 0.60 || safetyScore > 0.40 {
			reviewCount++
		}
	}

	fmt.Println("Go battery CSV audit")
	fmt.Printf("Candidate rows: %d\n", len(rows)-1)
	fmt.Printf("Chemistry count: %d\n", len(chemistries))
	fmt.Printf("Critical/safety review-like rows: %d\n", reviewCount)
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
