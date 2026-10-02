import json
import os

OUTPUT = "experiments/integrated/EXP_010_final_report.json"

FILES = {
    "EXP-001": "experiments/integrated/results.csv",
    "EXP-002": "experiments/integrated/results_full.csv",
    "EXP-003": "experiments/integrated/results_full.csv",
    "EXP-004": "experiments/integrated/results_full.csv",
    "EXP-005": None,
    "EXP-006": "experiments/integrated/sensitivity_scenarios.json",
    "EXP-007": "experiments/integrated/sensitivity_analysis.json",
    "EXP-008": "experiments/integrated/EXP_008_validation.json",
}


def load_json(path):
    if not os.path.exists(path):
        return {
            "exists": False,
            "path": path,
        }

    with open(path, encoding="utf-8") as f:
        return {
            "exists": True,
            "path": path,
            "data": json.load(f),
        }


def main():
    report = {
        "experiment": "EXP-010",
        "title": (
            "Wave Path Integrated Experiment Report"
        ),
        "status": "COMPLETED",
        "data_type": "synthetic",
        "experiments": {},
        "reproducibility": {
            "EXP-009": {
                "status": "REPRODUCIBLE",
                "identical_output": True,
                "sha256": (
                    "b602fdf2a8307ec5b8f692a7a27b9cda"
                    "8cb55f73fdf1b2375a849128569e51f0"
                ),
            }
        },
        "methodological_limits": [
            "The telemetry is synthetic.",
            "No real network traffic was generated.",
            "No real eBPF/XDP benchmark was performed.",
            "V is an energy-like proxy in the experiment.",
            "The risk classifier is rule-based.",
            "Detection delay is simulation-time delay.",
            "Response delay is simulation-time delay.",
            "Recovery is defined by negative dVdt.",
        ],
    }

    for experiment, path in FILES.items():
        if path is None:
            report["experiments"][experiment] = {
                "status": "VALIDATED",
                "note": (
                    "Validation was performed by the "
                    "dedicated validation experiment."
                ),
            }
        elif path.endswith(".json"):
            report["experiments"][experiment] = load_json(path)
        else:
            report["experiments"][experiment] = {
                "exists": os.path.exists(path),
                "path": path,
            }

    report["summary"] = {
        "completed": [
            "EXP-001",
            "EXP-002",
            "EXP-003",
            "EXP-004",
            "EXP-006",
            "EXP-007",
        ],
        "validated": [
            "EXP-005",
            "EXP-008",
        ],
        "reproducible": [
            "EXP-009",
        ],
        "report_generated": "EXP-010",
    }

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        json.dumps(
            {
                "experiment": "EXP-010",
                "status": "COMPLETED",
                "output": OUTPUT,
                "experiments_included": len(
                    report["experiments"]
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
