// Astrochemistry and the Molecular Universe
// Go region and molecular-family summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Region string
	Environment string
	MolecularFamily string
	ActivityIndex float64
	ComplexityScore float64
	IceScore float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"Taurus_TMC1", "cold_dark_cloud", "carbon_chain", 0.52, 0.55, 0.72},
		{"Orion_KL", "hot_core", "complex_organic", 0.61, 0.86, 0.48},
		{"TW_Hya", "disk_midplane", "ice_chemistry", 0.57, 0.60, 0.92},
		{"Comet_67P", "cometary_coma", "volatile_ice", 0.43, 0.44, 0.61},
		{"Titan", "planetary_atmosphere", "nitrile", 0.46, 0.70, 0.22},
	}

	sumActivity := map[string]float64{}
	sumComplexity := map[string]float64{}
	sumIce := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumActivity[r.MolecularFamily] += r.ActivityIndex
		sumComplexity[r.MolecularFamily] += r.ComplexityScore
		sumIce[r.MolecularFamily] += r.IceScore
		counts[r.MolecularFamily]++
	}

	file, err := os.Create("../outputs/tables/go_astrochemical_region_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "molecular_family,n,mean_activity_index,mean_complexity_score,mean_ice_score")

	for family, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			family,
			n,
			sumActivity[family]/float64(n),
			sumComplexity[family]/float64(n),
			sumIce[family]/float64(n),
		)
	}

	fmt.Println("Go astrochemical region summary complete.")
}
