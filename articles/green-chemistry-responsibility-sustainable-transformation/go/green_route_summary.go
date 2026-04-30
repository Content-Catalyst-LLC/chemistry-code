// Green Chemistry, Responsibility, and Sustainable Transformation
// Go route and chemistry-class summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Route struct {
	RouteName string
	ChemistryClass string
	GreenScore float64
	EFactor float64
	PMI float64
	HazardWeightedMassIntensity float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	routes := []Route{
		{"Route_A_Stoichiometric", "small_molecule_intermediate", 0.42, 14.00, 18.00, 10.4},
		{"Route_B_Catalytic", "small_molecule_intermediate", 0.70, 4.17, 7.50, 2.4},
		{"Route_C_Biocatalytic", "small_molecule_intermediate", 0.76, 3.33, 7.78, 1.7},
		{"Route_F_Flow_Chemistry", "specialty_chemical", 0.78, 3.00, 7.00, 1.9},
		{"Route_H_Circular_Material", "consumer_material", 0.77, 2.67, 6.33, 1.8},
	}

	sumScore := map[string]float64{}
	sumEFactor := map[string]float64{}
	sumPMI := map[string]float64{}
	counts := map[string]int{}

	for _, r := range routes {
		sumScore[r.ChemistryClass] += r.GreenScore
		sumEFactor[r.ChemistryClass] += r.EFactor
		sumPMI[r.ChemistryClass] += r.PMI
		counts[r.ChemistryClass]++
	}

	file, err := os.Create("../outputs/tables/go_green_route_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "chemistry_class,n,mean_green_score,mean_e_factor,mean_pmi")

	for className, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			className,
			n,
			sumScore[className]/float64(n),
			sumEFactor[className]/float64(n),
			sumPMI[className]/float64(n),
		)
	}

	fmt.Println("Go green route summary complete.")
}
