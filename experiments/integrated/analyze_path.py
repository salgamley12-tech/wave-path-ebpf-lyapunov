import csv
import json

INPUT = "experiments/integrated/results_full.csv"
OUTPUT = "experiments/integrated/path_analysis.json"


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
        r["authorized"] = r["authorized"].lower() == "true"

    max_v = max(rows, key=lambda r: r["V"])
    min_v = min(rows, key=lambda r: r["V"])

    max_rise = max(rows, key=lambda r: r["dVdt"])
    max_fall = min(rows, key=lambda r: r["dVdt"])

    negative = sum(1 for r in rows if r["dVdt"] < 0)
    positive = sum(1 for r in rows if r["dVdt"] > 0)
    zero = sum(1 for r in rows if r["dVdt"] == 0)

    unauthorized = [
        r for r in rows
        if not r["authorized"]
    ]

    drops = [
        r for r in rows
        if r["action"] == "drop"
    ]

    initial_v = rows[0]["V"]
    final_v = rows[-1]["V"]

    reduction_percent = (
        (initial_v - final_v) / initial_v * 100
        if initial_v != 0 else 0
    )

    analysis = {
        "experiment": "EXP-003",
        "samples": len(rows),

        "initial_V": initial_v,
        "final_V": final_v,
        "V_reduction_percent": reduction_percent,

        "maximum_V": {
            "value": max_v["V"],
            "t": max_v["t"],
        },

        "minimum_V": {
            "value": min_v["V"],
            "t": min_v["t"],
        },

        "maximum_positive_dVdt": {
            "value": max_rise["dVdt"],
            "t": max_rise["t"],
            "V": max_rise["V"],
            "risk": max_rise["risk"],
            "action": max_rise["action"],
        },

        "maximum_negative_dVdt": {
            "value": max_fall["dVdt"],
            "t": max_fall["t"],
            "V": max_fall["V"],
            "risk": max_fall["risk"],
            "action": max_fall["action"],
        },

        "dVdt_distribution": {
            "positive": positive,
            "negative": negative,
            "zero": zero,
        },

        "unauthorized": {
            "count": len(unauthorized),
            "first_t": unauthorized[0]["t"] if unauthorized else None,
            "last_t": unauthorized[-1]["t"] if unauthorized else None,
        },

        "drop_events": {
            "count": len(drops),
            "times": [r["t"] for r in drops],
        },
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)

    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
