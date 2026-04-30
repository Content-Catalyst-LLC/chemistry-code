// Chemistry, Classification, and the Human Understanding of Matter
// Go chemical class summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	AssignedClass string
	SampleName string
	EvidenceScore float64
	Reliability float64
	HazardScore float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"organic_molecular_substance", "ethyl_acetate_reference", 0.86, 0.88, 0.22},
		{"mixture_or_solution", "seawater_sample", 0.70, 0.75, 0.35},
		{"ionic_or_salt_crystal", "sodium_chloride_crystal", 0.86, 0.90, 0.18},
		{"polymer_material", "polyethylene_film", 0.78, 0.82, 0.20},
		{"heterogeneous_mixture", "soil_extract", 0.60, 0.62, 0.62},
	}

	sumEvidence := map[string]float64{}
	sumReliability := map[string]float64{}
	sumHazard := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumEvidence[r.AssignedClass] += r.EvidenceScore
		sumReliability[r.AssignedClass] += r.Reliability
		sumHazard[r.AssignedClass] += r.HazardScore
		counts[r.AssignedClass]++
	}

	file, err := os.Create("../outputs/tables/go_chemical_class_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "assigned_class,n,mean_evidence_score,mean_classification_reliability,mean_hazard_score")

	for className, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			className,
			n,
			sumEvidence[className]/float64(n),
			sumReliability[className]/float64(n),
			sumHazard[className]/float64(n),
		)
	}

	fmt.Println("Go chemical class summary complete.")
}
