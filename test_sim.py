
"""Check CARLA availability for simulation testing across multiple maps.

This script does not claim to run driving episodes. It records a blocked
status when CARLA is unavailable. Real driving metrics require a working
simulator and an implemented vehicle-driving loop.
"""

import csv
import time
from datetime import datetime
from pathlib import Path

import carla


PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs"
RESULTS_FILE = LOG_DIR / "sim_test_results.csv"

# Three maps to check. CARLA must have these maps installed.
MAPS = [
    "Town01",
    "Town02",
    "Town03",
]

CSV_FIELDS = [
    "timestamp",
    "map",
    "episode",
    "status",
    "collision",
    "completion_time_seconds",
    "average_speed_kmh",
    "details",
]


def check_map(client, map_name):
    """Check whether CARLA can load a map; do not claim a driving test."""
    started = time.perf_counter()

    try:
        world = client.load_world(map_name)
        loaded_map = world.get_map().name

        return {
            "status": "MAP_LOADED_ONLY",
            "collision": "",
            "completion_time_seconds": "",
            "average_speed_kmh": "",
            "details": (
                f"Loaded {loaded_map}; no driving episode or "
                "collision measurement was performed."
            ),
            "elapsed_seconds": round(time.perf_counter() - started, 2),
        }

    except Exception as exc:
        return {
            "status": "MAP_LOAD_FAILED",
            "collision": "",
            "completion_time_seconds": "",
            "average_speed_kmh": "",
            "details": str(exc),
            "elapsed_seconds": round(time.perf_counter() - started, 2),
        }


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_exists = RESULTS_FILE.exists() and RESULTS_FILE.stat().st_size > 0

    with RESULTS_FILE.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)

        if not file_exists:
            writer.writeheader()

        try:
            client = carla.Client("localhost", 2000)
            client.set_timeout(10.0)
            client.get_world()
            print("Connected to CARLA.")

        except Exception as exc:
            print(f"CARLA connection failed: {exc}")

            for map_name in MAPS:
                writer.writerow({
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "map": map_name,
                    "episode": 1,
                    "status": "BLOCKED_NO_CONNECTION",
                    "collision": "",
                    "completion_time_seconds": "",
                    "average_speed_kmh": "",
                    "details": str(exc),
                })

            print(f"Blocked test records saved to: {RESULTS_FILE}")
            return

        for map_name in MAPS:
            print(f"\nChecking {map_name}...")

            result = check_map(client, map_name)

            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "map": map_name,
                "episode": 1,
                "status": result["status"],
                "collision": result["collision"],
                "completion_time_seconds": result["completion_time_seconds"],
                "average_speed_kmh": result["average_speed_kmh"],
                "details": result["details"],
            })

            print("Status:", result["status"])
            print("Details:", result["details"])

    print(f"\nResults saved to: {RESULTS_FILE}")
    print("Note: loading a map is not the same as completing a driving episode.")


if __name__ == "__main__":
    main()

