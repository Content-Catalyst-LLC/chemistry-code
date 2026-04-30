// Ocean Chemistry and the Carbonate System
// Go ocean-region and monitoring summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Region string
	WaterMass string
	CarbonatePressure float64
	AcidificationPressure float64
	DeoxygenationPressure float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"North_Atlantic", "surface_subpolar", 0.14, 0.18, 0.00},
		{"Equatorial_Pacific", "surface_upwelling", 0.29, 0.34, 0.00},
		{"North_Pacific", "intermediate_water", 0.57, 0.65, 0.39},
		{"Arabian_Sea", "oxygen_minimum_zone", 0.82, 0.88, 0.90},
		{"Caribbean_Reef", "surface_tropical", 0.07, 0.08, 0.00},
	}

	sumCarbonate := map[string]float64{}
	sumAcid := map[string]float64{}
	sumDeoxy := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumCarbonate[r.WaterMass] += r.CarbonatePressure
		sumAcid[r.WaterMass] += r.AcidificationPressure
		sumDeoxy[r.WaterMass] += r.DeoxygenationPressure
		counts[r.WaterMass]++
	}

	file, err := os.Create("../outputs/tables/go_ocean_region_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "water_mass,n,mean_carbonate_pressure,mean_acidification_pressure,mean_deoxygenation_pressure")

	for waterMass, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			waterMass,
			n,
			sumCarbonate[waterMass]/float64(n),
			sumAcid[waterMass]/float64(n),
			sumDeoxy[waterMass]/float64(n),
		)
	}

	fmt.Println("Go ocean region summary complete.")
}
