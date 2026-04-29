package main

import (
	"fmt"
	"math"
)

type AtmosphericRecord struct {
	Site           string
	Analyte        string
	ClassName      string
	Concentration  float64
	Unit           string
	ReferenceValue float64
}

func RatioToReference(concentration float64, referenceValue float64) float64 {
	return concentration / referenceValue
}

func CO2Forcing(currentPPM float64, referencePPM float64) float64 {
	return 5.35 * math.Log(currentPPM/referencePPM)
}

func FirstOrderConcentration(c0 float64, kPerDay float64, tDays float64) float64 {
	return c0 * math.Exp(-kPerDay*tDays)
}

func main() {
	records := []AtmosphericRecord{
		{"Background-A", "CO2", "long_lived_greenhouse_gas", 423.0, "ppm", 280.0},
		{"Urban-B", "O3", "secondary_pollutant", 0.074, "ppm", 0.070},
		{"Urban-B", "PM2.5", "aerosol_particle", 17.2, "ug/m3", 15.0},
	}

	fmt.Println("Atmospheric chemistry screening example")
	for _, record := range records {
		ratio := RatioToReference(record.Concentration, record.ReferenceValue)
		flag := "at_or_below_reference"
		if ratio > 1.0 {
			flag = "above_reference"
		}
		fmt.Printf(
			"%s | %s | %s | %.4f %s | ratio %.3f | %s\n",
			record.Site,
			record.Analyte,
			record.ClassName,
			record.Concentration,
			record.Unit,
			ratio,
			flag,
		)
	}

	forcing := CO2Forcing(423.0, 280.0)
	fmt.Printf("\nApproximate CO2 forcing: %.3f W/m2\n", forcing)

	fmt.Println("\nFirst-order atmospheric decay")
	for day := 0.0; day <= 30.0; day += 5.0 {
		fmt.Printf("day %.0f: %.3f ppb\n", day, FirstOrderConcentration(100.0, 0.20, day))
	}
}
