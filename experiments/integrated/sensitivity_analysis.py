import csv
import json

INPUT = "experiments/integrated/results_full.csv"
OUTPUT = "experiments/integrated/sensitivity_analysis.json"


def classify_scenario(rows):
    low = []
    medium = []
    high = []

    for r in rows:
        score = float(r["anomaly_score"])

        if score < 0.50:
            low.append(r)
        elif score < 0.85:
            medium.append(r)
        else:
            high.append(r)

    return {
        "low_anomaly": len(low),
        "medium_anomaly": len(medium),
        "high_anomaly": len(high),
    }


def main():
    with open(INPUT, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise RuntimeError("No data found")

    for r in rows:
        r["t"] = float(r["t"])
        r["V"] = float(r["V"])
        r["dVdt"] = float(r["dVdt"])
        r["anomaly_score"] = float(r["anomaly_score"])

    v_values = [r["V"] for r in rows]
    dv_values = [r["dVdt"] for r in rows]

    result = {
        "experiment": "EXP-006",
        "description": "Sensitivity analysis of the existing synthetic run",
        "samples": len(rows),

        "V": {
            "initial": v_values[0],
            "final": v_values[-1],
            "minimum": min(v_values),
            "maximum": max(v_values),
        },

        "dVdt": {
            "minimum": min(dv_values),
            "maximum": max(dv_values),
        },

        "anomaly_distribution": classify_scenario(rows),

        "risk_distribution": {
            "low": sum(1 for r in rows if r["risk"] == "low"),
            "medium": sum(1 for r in rows if r["risk"] == "medium"),
            "high": sum(1 for r in rows if r["risk"] == "high"),
        },

        "action_distribution": {
            "pass": sum(1 for r in rows if r["action"] == "pass"),
            "observe_only": sum(
                1 for r in rows
                if r["action"] == "observe_only"
            ),
            "drop": sum(
                1 for r in rows
                if r["action"] == "drop"
            ),
        },
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
