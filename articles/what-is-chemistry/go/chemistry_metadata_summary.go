package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

// Portable summary helper for introductory chemistry examples.
func main() {
	path := filepath.Join("data", "intro_chemistry_examples.csv")

	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		panic(err)
	}

	fmt.Printf("intro_chemistry_examples=%d\n", len(records)-1)
}
