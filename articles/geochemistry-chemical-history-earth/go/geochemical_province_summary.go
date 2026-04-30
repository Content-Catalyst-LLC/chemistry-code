// Geochemistry and the Chemical History of Earth
// Go geochemical province and rock-type summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Sample struct {
	SampleID string
	Province string
	RockType string
	TectonicSetting string
	GeochemicalPressure float64
	WeatheringIndex float64
	RedoxState float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	samples := []Sample{
		{"GEOFS001", "Superior_Craton", "granite", "continental_crust", 0.34, 0.17, 0.25},
		{"GEOFS002", "Mid_Ocean_Ridge", "basalt", "oceanic_crust", 0.28, 0.18, 0.52},
		{"GEOFS005", "Himalayan_Foreland", "shale", "sedimentary_basin", 0.55, 0.42, 0.30},
		{"GEOFS006", "Banded_Iron_Formation", "iron_formation", "precambrian_ocean", 0.62, 0.00, 0.92},
		{"GEOFS008", "Siberian_Platform", "carbonate", "marine_sedimentary", 0.24, 0.00, 0.32},
	}

	sumPressure := map[string]float64{}
	sumWeathering := map[string]float64{}
	sumRedox := map[string]float64{}
	counts := map[string]int{}

	for _, s := range samples {
		sumPressure[s.TectonicSetting] += s.GeochemicalPressure
		sumWeathering[s.TectonicSetting] += s.WeatheringIndex
		sumRedox[s.TectonicSetting] += s.RedoxState
		counts[s.TectonicSetting]++
	}

	file, err := os.Create("../outputs/tables/go_geochemical_province_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "tectonic_setting,n,mean_geochemical_pressure,mean_weathering_index,mean_redox_state")

	for setting, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			setting,
			n,
			sumPressure[setting]/float64(n),
			sumWeathering[setting]/float64(n),
			sumRedox[setting]/float64(n),
		)
	}

	fmt.Println("Go geochemical province summary complete.")
}
