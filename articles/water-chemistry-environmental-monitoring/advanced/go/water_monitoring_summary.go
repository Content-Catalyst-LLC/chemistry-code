// Water Chemistry and Environmental Monitoring
// Go monitoring-network and water-body summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Site string
	WaterBody string
	Analyte string
	PressureIndex float64
	LoadKgDay float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"River-A", "river", "nitrate_as_N", 0.42, 552.5},
		{"Lake-B", "lake", "dissolved_oxygen", 0.47, 0.0},
		{"Well-C", "aquifer", "arsenic", 0.56, 0.005},
		{"Storm-D", "urban_runoff", "lead", 0.72, 0.327},
		{"Estuary-E", "estuary", "copper", 0.58, 1.693},
	}

	sumPressure := map[string]float64{}
	sumLoad := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumPressure[r.WaterBody] += r.PressureIndex
		sumLoad[r.WaterBody] += r.LoadKgDay
		counts[r.WaterBody]++
	}

	file, err := os.Create("../outputs/tables/go_water_monitoring_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "water_body,n,mean_pressure_index,total_load_kg_day")

	for waterBody, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f\n",
			waterBody,
			n,
			sumPressure[waterBody]/float64(n),
			sumLoad[waterBody],
		)
	}

	fmt.Println("Go water monitoring summary complete.")
}
