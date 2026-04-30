// Atmospheric Chemistry and Climate Processes
// Go atmospheric monitoring and chemical-class summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Station string
	ChemicalClass string
	Species string
	PressureIndex float64
	ForcingProxy float64
	OzoneIndex float64
	AerosolEffect float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"Global-CO2", "greenhouse_gas", "CO2", 0.71, 2.21, 0.0, -0.95},
		{"Global-CH4", "greenhouse_gas", "CH4", 0.62, 0.64, 0.0, -0.70},
		{"Urban-O3", "secondary_pollutant", "O3", 0.48, 0.0, 65.2, -1.78},
		{"Wildfire-PM", "aerosol", "PM2.5", 0.73, 0.0, 34.3, -14.2},
		{"Dust-AOD", "aerosol", "coarse_aerosol", 0.69, 0.0, 7.8, -18.2},
	}

	sumPressure := map[string]float64{}
	sumForcing := map[string]float64{}
	sumOzone := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumPressure[r.ChemicalClass] += r.PressureIndex
		sumForcing[r.ChemicalClass] += r.ForcingProxy
		sumOzone[r.ChemicalClass] += r.OzoneIndex
		counts[r.ChemicalClass]++
	}

	file, err := os.Create("../outputs/tables/go_atmospheric_monitoring_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "chemical_class,n,mean_pressure_index,mean_forcing_proxy,mean_ozone_index")

	for className, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			className,
			n,
			sumPressure[className]/float64(n),
			sumForcing[className]/float64(n),
			sumOzone[className]/float64(n),
		)
	}

	fmt.Println("Go atmospheric monitoring summary complete.")
}
