// Toxicology, Exposure, and Chemical Risk
// Go route-level exposure summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Chemical string
	Route string
	TargetSystem string
	HazardQuotient float64
	VulnerabilityFactor float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"arsenic", "ingestion", "cancer_and_skin", 0.030, 1.20},
		{"lead", "ingestion", "neurodevelopment", 0.120, 1.80},
		{"mercury", "ingestion", "neurodevelopment", 0.420, 1.50},
		{"benzene", "inhalation", "bone_marrow", 0.080, 1.10},
		{"ozone", "inhalation", "respiratory", 0.190, 1.25},
	}

	routeHI := map[string]float64{}
	routeAdjusted := map[string]float64{}

	for _, r := range records {
		routeHI[r.Route] += r.HazardQuotient
		routeAdjusted[r.Route] += r.HazardQuotient * r.VulnerabilityFactor
	}

	file, err := os.Create("../outputs/tables/go_toxicology_route_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "route,hazard_index,vulnerability_adjusted_hazard_index")

	for route, hi := range routeHI {
		fmt.Fprintf(file, "%s,%.6f,%.6f\n", route, hi, routeAdjusted[route])
	}

	fmt.Println("Go toxicology route summary complete.")
}
