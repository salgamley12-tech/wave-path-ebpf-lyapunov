import csv
import json

INPUT = "experiments/integrated/sensitivity_scenarios.csv"
OUTPUT = "experiments/integrated/sensitivity_analysis.json"

DISTURBANCE_END = {
    "low": 1.2,
    "medium": 1.4,
    "high": 1.6,
}

DISTURBANCE_START = 1.0


def first_time(rows, condition):
    for row in rows:
        if condition(row):
            return float(row["t"])
    return None


def analyze(scenario, rows):
    end = DISTURBANCE_END[scenario]

    first_high = first_time(
        rows,
        lambda r: r["risk"] == "high",
    )

    first_drop = first_time(
        rows,
        lambda r: r["action"] == "drop",
    )

    recovery_rows = [
        r for r in rows
        if float(r["t"]) > end
    ]

    recovery_start = first_time(
        recovery_rows,
        lambda r: float(r["dVdt"]) < 0,
    )

    max_v = max(
        rows,
        key=lambda r: float(r["V"]),
    )

    min_v = min(
        rows,
        key=lambda r: float(r["V"]),
    )

    max_dvdt = max(
        rows,
        key=lambda r: float(r["dVdt"]),
    )

    result = {
        "samples": len(rows),
        "disturbance_start": DISTURBANCE_START,
        "disturbance_end": end,
        "maximum_V": {
            "value": float(max_v["V"]),
            "t": float(max_v["t"]),
        },
        "minimum_V": {
            "value": float(min_v["V"]),
            "t": float(min_v["t"]),
        },
        "maximum_dVdt": {
            "value": float(max_dvdt["dVdt"]),
            "t": float(max_dvdt["t"]),
        },
        "first_high": first_high,
        "first_drop": first_drop,
        "recovery_start": recovery_start,
    }

    if first_high is not None:
        result["detection_delay"] = (
            first_high - DISTURBANCE_START
        )
    else:
        result["detection_delay"] = None

    if first_drop is not None:
        result["response_delay"] = (
            first_drop - DISTURBANCE_START
        )
    else:
        result["response_delay"] = None

    if recovery_start is not None:
        result["recovery_delay"] = (
            recovery_start - end
        )
    else:
        result["recovery_delay"] = None

    return result


def main():
    grouped = {}

    with open(
        INPUT,
        newline="",
        encoding="utf-8",
    ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            grouped.setdefault(
                row["scenario"],
                [],
            ).append(row)

    analysis = {
        "experiment": "EXP-007",
        "description": (
            "Corrected sensitivity response "
            "and recovery analysis"
        ),
        "method_note": (
            "Recovery is defined as the first "
            "negative dVdt after the scenario-specific "
            "disturbance end."
        ),
        "scenarios": {},
    }

    for scenario, rows in grouped.items():
        analysis["scenarios"][scenario] = analyze(
            scenario,
            rows,
        )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            analysis,
            f,
            indent=2,
        )

    print(
        json.dumps(
            analysis,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
