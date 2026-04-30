// Chemistry, Ethics, and the Governance of Molecular Power
// Go governance-domain summary.
// Synthetic educational code only.

package main

import (
	"fmt"
	"os"
)

type Record struct {
	Domain string
	Context string
	Risk float64
	JusticeRisk float64
	GovernanceGap float64
	ResponsibleScore float64
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	records := []Record{
		{"medicine", "essential_therapeutic", 0.18, 0.21, 0.04, 0.72},
		{"agriculture", "high_volume_pesticide", 0.46, 0.58, 0.26, 0.43},
		{"industrial_material", "persistent_additive", 0.52, 0.67, 0.39, 0.31},
		{"consumer_product", "indoor_exposure_chemical", 0.42, 0.55, 0.34, 0.28},
		{"dual_use", "restricted_toxic_precursor", 0.50, 0.62, 0.07, 0.20},
	}

	sumRisk := map[string]float64{}
	sumGap := map[string]float64{}
	sumScore := map[string]float64{}
	counts := map[string]int{}

	for _, r := range records {
		sumRisk[r.Domain] += r.JusticeRisk
		sumGap[r.Domain] += r.GovernanceGap
		sumScore[r.Domain] += r.ResponsibleScore
		counts[r.Domain]++
	}

	file, err := os.Create("../outputs/tables/go_molecular_power_summary.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "domain,n,mean_justice_weighted_risk,mean_governance_gap,mean_responsible_score")

	for domain, n := range counts {
		fmt.Fprintf(
			file,
			"%s,%d,%.6f,%.6f,%.6f\n",
			domain,
			n,
			sumRisk[domain]/float64(n),
			sumGap[domain]/float64(n),
			sumScore[domain]/float64(n),
		)
	}

	fmt.Println("Go molecular power summary complete.")
}
