// Environmental Chemistry and the Chemical Conditions of Habitability
// Go compartment and pathway summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Site string
	Compartment string
	AnalyteClass string
	PressureIndex float64
	ExposureWeight float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"Groundwater-B", "groundwater", "metalloid", 0.68, 0.95},
		{"Sediment-D", "sediment", "pah", 0.48, 0.55},
		{"Stormwater-F", "stormwater", "metal", 0.57, 0.72},
		{"Wetland-G", "wetland_water", "nutrient", 0.52, 0.62},
		{"Groundwater-I", "groundwater", "chlorinated_solvent", 0.72, 0.93},
	}

	sumPressure := map[string]float64{}
	sumExposure := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumPressure[r.Compartment] += r.PressureIndex
		sumExposure[r.Compartment] += r.ExposureWeight
		counts[r.Compartment]++
	}

	file, err := os.Create("../outputs/tables/go_environmental_compartment_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "compartment,n,mean_pressure_index,mean_exposure_weight")

	for compartment, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f\n",
			compartment,
			n,
			sumPressure[compartment]/float64(n),
			sumExposure[compartment]/float64(n),
		)
	}

	fmt.Println("Go environmental compartment summary complete.")
}
