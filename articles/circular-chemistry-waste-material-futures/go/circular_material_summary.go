// Circular Chemistry, Waste, and Material Futures
// Go material-class summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Stream struct {
	MaterialClass string
	StreamName string
	RecoveryYield float64
	CircularRetention float64
	SafeCircularity float64
	CircularScore float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	streams := []Stream{
		{"polymer", "PET_bottles_clear", 0.76, 0.45, 0.82, 0.68},
		{"polymer", "Multilayer_film", 0.42, 0.11, 0.58, 0.34},
		{"metal", "Aluminum_scrap", 0.90, 0.78, 0.86, 0.82},
		{"battery", "Lithium_ion_batteries", 0.62, 0.35, 0.48, 0.47},
		{"solvent", "Solvent_wash_stream", 0.84, 0.64, 0.62, 0.72},
	}

	sumRecovery := map[string]float64{}
	sumRetention := map[string]float64{}
	sumSafety := map[string]float64{}
	sumScore := map[string]float64{}
	counts := map[string]int{}

	for _, s := range streams {
		sumRecovery[s.MaterialClass] += s.RecoveryYield
		sumRetention[s.MaterialClass] += s.CircularRetention
		sumSafety[s.MaterialClass] += s.SafeCircularity
		sumScore[s.MaterialClass] += s.CircularScore
		counts[s.MaterialClass]++
	}

	file, err := os.Create("../outputs/tables/go_circular_material_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "material_class,n,mean_recovery_yield,mean_circular_retention,mean_safe_circularity,mean_circular_score")

	for className, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f,%.6f\n",
			className,
			n,
			sumRecovery[className]/float64(n),
			sumRetention[className]/float64(n),
			sumSafety[className]/float64(n),
			sumScore[className]/float64(n),
		)
	}

	fmt.Println("Go circular material summary complete.")
}
