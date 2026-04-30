// Medicinal Chemistry and Drug Discovery
// Go project analytics example.
// Synthetic educational code only.

package main

import (
	"fmt"
	"math"
	"os"
)

type Candidate struct {
	CompoundID string
	Project string
	IC50nM float64
	OffTargetIC50nM float64
	CLogP float64
}

func pIC50(ic50nM float64) float64 {
	return -math.Log10(ic50nM * 1e-9)
}

func LLE(c Candidate) float64 {
	return pIC50(c.IC50nM) - c.CLogP
}

func Selectivity(c Candidate) float64 {
	if c.IC50nM <= 0 {
		return 0
	}
	return c.OffTargetIC50nM / c.IC50nM
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	candidates := []Candidate{
		{"MEDADV001", "Kinase-A", 18, 2100, 3.2},
		{"MEDADV002", "Kinase-A", 42, 980, 4.1},
		{"MEDADV003", "GPCR-B", 7, 320, 2.8},
		{"MEDADV010", "GPCR-B", 22, 650, 3.1},
		{"MEDADV006", "Enzyme-E", 32, 5200, 1.9},
	}

	file, err := os.Create("../outputs/tables/go_medicinal_project_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "compound_id,project,pIC50,LLE,selectivity_window")

	for _, c := range candidates {
		fmt.Fprintf(
			file,
			"%s,%s,%.6f,%.6f,%.6f\n",
			c.CompoundID,
			c.Project,
			pIC50(c.IC50nM),
			LLE(c),
			Selectivity(c),
		)
	}

	fmt.Println("Go medicinal project summary complete.")
}
