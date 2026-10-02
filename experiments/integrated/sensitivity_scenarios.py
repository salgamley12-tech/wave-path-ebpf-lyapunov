import csv
import json

OUTPUT_CSV = "experiments/integrated/sensitivity_scenarios.csv"
OUTPUT_JSON = "experiments/integrated/sensitivity_scenarios.json"

SCENARIOS = {
    "low": {
        "burst_start": 1.0,
        "burst_end": 1.2,
        "burst_multiplier": 2.0,
        "unauthorized": False,
    },
    "medium": {
        "burst_start": 1.0,
        "burst_end": 1.4,
        "burst_multiplier": 4.0,
        "unauthorized": True,
    },
    "high": {
        "burst_start": 1.0,
        "burst_end": 1.6,
        "burst_multiplier": 7.0,
        "unauthorized": True,
    },
}


def classify_risk(dvdt, anomaly):
    if dvdt > 0 or anomaly >= 0.85:
        return "high"
    if anomaly >= 0.50:
        return "medium"
    return "low"


def choose_action(risk, authorized):
    if not authorized:
        return "observe_only"
    if risk == "high":
        return "drop"
    return "pass"


def run_scenario(name, config, samples=200):
    rows = []
    previous_v = None
    previous_t = None

    for i in range(samples):
        t = i * 0.01

        in_burst = (
            config["burst_start"]
            <= t
            <= config["burst_end"]
        )

        if in_burst:
            bytes_value = (
                100.0 * config["burst_multiplier"]
            )
        else:
            bytes_value = 100.0

        connection_rate = 10.0

        bytes_rate = bytes_value / 0.1

        anomaly = 0.0

        if in_burst:
            anomaly += min(
                0.25,
                (bytes_value - 100.0) / 2000.0,
            )

        if config["unauthorized"]:
            anomaly += 0.75

        anomaly = min(anomaly, 1.0)

        u = bytes_rate / 100.0
        v = connection_rate / 10.0

        V = 0.5 * (v * v + u * u)

        if previous_v is None:
            dvdt = 0.0
        else:
            dt = t - previous_t
            dvdt = (V - previous_v) / dt

        risk = classify_risk(dvdt, anomaly)

        action = choose_action(
            risk,
            not config["unauthorized"],
        )

        rows.append({
            "scenario": name,
            "t": t,
            "bytes_rate": bytes_rate,
            "connection_rate": connection_rate,
            "anomaly_score": anomaly,
            "V": V,
            "dVdt": dvdt,
            "risk": risk,
            "action": action,
            "authorized": not config["unauthorized"],
        })

        previous_v = V
        previous_t = t

    return rows


def main():
    all_rows = []

    for name, config in SCENARIOS.items():
        rows = run_scenario(name, config)
        all_rows.extend(rows)

    fieldnames = [
        "scenario",
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

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(all_rows)

    summary = {}

    for scenario in SCENARIOS:
        rows = [
            r for r in all_rows
            if r["scenario"] == scenario
        ]

        summary[scenario] = {
            "samples": len(rows),
            "max_V": max(r["V"] for r in rows),
            "min_V": min(r["V"] for r in rows),
            "max_dVdt": max(r["dVdt"] for r in rows),
            "risk_counts": {},
            "action_counts": {},
        }

        for row in rows:
            risk = row["risk"]
            action = row["action"]

            summary[scenario]["risk_counts"][risk] = (
                summary[scenario]["risk_counts"].get(risk, 0)
                + 1
            )

            summary[scenario]["action_counts"][action] = (
                summary[scenario]["action_counts"].get(action, 0)
                + 1
            )

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            {
                "experiment": "EXP-006",
                "description": (
                    "Sensitivity scenarios"
                    " for synthetic disturbances"
                ),
                "summary": summary,
            },
            f,
            indent=2,
        )

    print(
        json.dumps(
            {
                "experiment": "EXP-006",
                "scenarios": list(SCENARIOS.keys()),
                "csv": OUTPUT_CSV,
                "json": OUTPUT_JSON,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
