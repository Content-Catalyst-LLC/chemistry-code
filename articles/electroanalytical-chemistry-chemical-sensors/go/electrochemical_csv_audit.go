package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dataPath := filepath.Join("..", "data", "sensor_calibration.csv")

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

	analytes := map[string]bool{}
	electrodes := map[string]bool{}
	methods := map[string]bool{}

	for _, row := range rows[1:] {
		if len(row) != 6 {
			panic("malformed sensor calibration row")
		}
		analytes[row[1]] = true
		electrodes[row[4]] = true
		methods[row[5]] = true
	}

	fmt.Println("Go electrochemical sensor CSV audit")
	fmt.Printf("Calibration rows: %d\n", len(rows)-1)
	fmt.Printf("Analyte count: %d\n", len(analytes))
	fmt.Printf("Electrode count: %d\n", len(electrodes))
	fmt.Printf("Method count: %d\n", len(methods))
	fmt.Println("Responsible-use note: synthetic educational data only.")
}
