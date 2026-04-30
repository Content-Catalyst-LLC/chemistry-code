// Soil Chemistry, Nutrient Cycles, and Land Systems
// Go soil-region and land-use summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Site string
	LandUse string
	SoilPressure float64
	LeachingPressure float64
	CarbonStability float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"Prairie-A", "cropland", 0.24, 0.16, 0.66},
		{"Field-B", "intensive_cropland", 0.43, 0.48, 0.28},
		{"Irrigated-C", "irrigated_agriculture", 0.45, 0.34, 0.30},
		{"Forest-D", "forest", 0.19, 0.17, 0.82},
		{"Degraded-E", "degraded_land", 0.71, 0.66, 0.13},
	}

	sumPressure := map[string]float64{}
	sumLeaching := map[string]float64{}
	sumCarbon := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumPressure[r.LandUse] += r.SoilPressure
		sumLeaching[r.LandUse] += r.LeachingPressure
		sumCarbon[r.LandUse] += r.CarbonStability
		counts[r.LandUse]++
	}

	file, err := os.Create("../outputs/tables/go_soil_land_use_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "land_use,n,mean_soil_pressure,mean_leaching_pressure,mean_carbon_stability")

	for landUse, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			landUse,
			n,
			sumPressure[landUse]/float64(n),
			sumLeaching[landUse]/float64(n),
			sumCarbon[landUse]/float64(n),
		)
	}

	fmt.Println("Go soil land-use summary complete.")
}
