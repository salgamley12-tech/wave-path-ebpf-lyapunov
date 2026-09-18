import csv
import json

from ai.risk import classify
from policy.policy import guard


INPUT = "experiments/integrated/results.csv"
OUTPUT = "experiments/integrated/results_full.csv"
SUMMARY = "experiments/integrated/analysis_summary.json"


def main():
    rows = []

    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        previous_v = None
        previous_t = None

        for r in reader:
            t = float(r["t"])
            V = float(r["V"])
            anomaly = float(r["anomaly_score"])
            authorized = r["authorized"].lower() == "true"

            if previous_v is None:
                dVdt = 0.0
            else:
                dt = t - previous_t
                dVdt = (V - previous_v) / dt

            risk = classify(dVdt, anomaly)
            action = guard(risk, authorized)

            rows.append({
                "t": t,
                "bytes_rate": float(r["bytes_rate"]),
                "connection_rate": float(r["connection_rate"]),
                "anomaly_score": anomaly,
                "V": V,
                "dVdt": dVdt,
                "risk": risk.value,
                "action": action.value,
                "authorized": authorized,
            })

            previous_v = V
            previous_t = t

    fields = [
        "t",
        "bytes_rate",
        "connection_rate",
        "anomaly_score",
        "V",
        "dVdt",
        "risk",
        "action",
        "authorized",
    ]

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    risk_counts = {}
    action_counts = {}

    for r in rows:
        risk_counts[r["risk"]] = risk_counts.get(r["risk"], 0) + 1
        action_counts[r["action"]] = action_counts.get(r["action"], 0) + 1

    V_values = [r["V"] for r in rows]
    dVdt_values = [r["dVdt"] for r in rows]

    increasing = sum(1 for x in dVdt_values if x > 0)
    decreasing = sum(1 for x in dVdt_values if x < 0)
    stable = sum(1 for x in dVdt_values if x == 0)

    summary = {
        "experiment": "EXP-002",
        "input": INPUT,
        "output": OUTPUT,
        "samples": len(rows),
        "initial_V": V_values[0],
        "final_V": V_values[-1],
        "minimum_V": min(V_values),
        "maximum_V": max(V_values),
        "positive_dVdt": increasing,
        "negative_dVdt": decreasing,
        "zero_dVdt": stable,
        "risk_counts": risk_counts,
        "action_counts": action_counts,
        "unauthorized_events": sum(
            1 for r in rows if not r["authorized"]
        ),
    }

    with open(SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
