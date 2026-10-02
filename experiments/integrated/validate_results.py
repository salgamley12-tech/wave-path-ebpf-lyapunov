import csv
import json

INPUT = "experiments/integrated/results_full.csv"
OUTPUT = "experiments/integrated/validation_report.json"


EXPECTED = {
    "samples": 200,
    "initial_V": 505000.0,
    "final_V": 63419.005,
    "unauthorized_events": 51,
    "risk_counts": {
        "low": 147,
        "high": 53,
    },
    "action_counts": {
        "pass": 147,
        "observe_only": 51,
        "drop": 2,
    },
}


def close(a, b, tolerance=1e-9):
    return abs(a - b) <= tolerance


def main():
    with open(INPUT, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise RuntimeError("No data found")

    risk_counts = {}
    action_counts = {}

    for row in rows:
        risk = row["risk"]
        action = row["action"]

        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        action_counts[action] = action_counts.get(action, 0) + 1

    actual = {
        "samples": len(rows),
        "initial_V": float(rows[0]["V"]),
        "final_V": float(rows[-1]["V"]),
        "unauthorized_events": sum(
            1 for r in rows
            if r["authorized"].lower() == "false"
        ),
        "risk_counts": risk_counts,
        "action_counts": action_counts,
    }

    checks = {
        "samples": actual["samples"] == EXPECTED["samples"],
        "initial_V": close(
            actual["initial_V"],
            EXPECTED["initial_V"]
        ),
        "final_V": close(
            actual["final_V"],
            EXPECTED["final_V"]
        ),
        "unauthorized_events": (
            actual["unauthorized_events"]
            == EXPECTED["unauthorized_events"]
        ),
        "risk_counts": (
            actual["risk_counts"]
            == EXPECTED["risk_counts"]
        ),
        "action_counts": (
            actual["action_counts"]
            == EXPECTED["action_counts"]
        ),
    }

    validation_passed = all(checks.values())

    report = {
        "experiment": "EXP-005",
        "validation_passed": validation_passed,
        "expected": EXPECTED,
        "actual": actual,
        "checks": checks,
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
