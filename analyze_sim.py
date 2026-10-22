
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
CSV_FILE = ROOT / "logs" / "sim_test_results.csv"
PLOT_FILE = ROOT / "reports" / "sim_test_status.png"


def main():
    if not CSV_FILE.exists():
        print(f"Results file not found: {CSV_FILE}")
        return

    df = pd.read_csv(CSV_FILE)

    print("\nSimulation Test Results")
    print(df[["map", "episode", "status"]].to_string(index=False))

    print("\nStatus counts:")
    print(df["status"].value_counts().to_string())

    completed = df[df["status"] == "COMPLETED"].copy()

    if completed.empty:
        print("\nNo completed driving episodes.")
        print("Performance metrics cannot be calculated yet.")
    else:
        completed["collision"] = (
            completed["collision"].astype(str).str.lower() == "true"
        )
        print(f"\nMeasured episodes: {len(completed)}")
        print(f"Collision rate: {completed['collision'].mean() * 100:.2f}%")
        print(
            "Mean completion time (seconds):",
            pd.to_numeric(
                completed["completion_time_seconds"]
            ).mean(),
        )
        print(
            "Mean average speed (km/h):",
            pd.to_numeric(completed["average_speed_kmh"]).mean(),
        )

    df["status"].value_counts().plot(kind="bar", rot=0)
    plt.title("CARLA Simulation Test Status")
    plt.xlabel("Status")
    plt.ylabel("Number of records")
    plt.tight_layout()

    PLOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(PLOT_FILE, dpi=150)
    plt.close()

    print(f"\nPlot saved to: {PLOT_FILE}")


if __name__ == "__main__":
    main()
