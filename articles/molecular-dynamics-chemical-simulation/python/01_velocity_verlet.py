"""
Calculate a simple velocity-Verlet-style molecular dynamics update.

Run from article directory:
    python python/01_velocity_verlet.py
"""

from pathlib import Path
import pandas as pd

from molecular_dynamics_core import velocity_verlet_step


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "particles_initial.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "velocity_verlet.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = velocity_verlet_step(data, dt=0.5)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
