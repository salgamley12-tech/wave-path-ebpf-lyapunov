import csv
import json
import math
import os

INPUT_CSV = "experiments/integrated/sensitivity_scenarios.csv"
INPUT_JSON = "experiments/integrated/sensitivity_analysis.json"
OUTPUT = "experiments/integrated/EXP_008_validation.json"


def check(condition):
    return bool(condition)


def main():
    checks = {}

    checks["csv_exists"] = os.path.exists(INPUT_CSV)
    checks["json_exists"] = os.path.exists(INPUT_JSON)

    with open(
        INPUT_CSV,
        newline="",
        encoding="utf-8",
    ) as f:
        rows = list(csv.DictReader(f))

    checks["total_samples"] = check(len(rows) == 600)

    scenarios = {}

    for row in rows:
        scenarios.setdefault(
            row["scenario"],
            [],
        ).append(row)

    checks["three_scenarios"] = check(
        set(scenarios) == {"low", "medium", "high"}
    )

    checks["200_samples_each"] = check(
        all(
            len(scenarios[name]) == 200
            for name in ("low", "medium", "high")
        )
    )

    numeric_fields = [
        "t",
        "bytes_rate",
        "connection_rate",
        "anomaly_score",
        "V",
        "dVdt",
    ]

    no_nan = True

    for row in rows:
        for field in numeric_fields:
            try:
                value = float(row[field])
                if not math.isfinite(value):
                    no_nan = False
            except (ValueError, TypeError):
                no_nan = False

    checks["finite_numeric_values"] = check(no_nan)

    with open(
        INPUT_JSON,
        encoding="utf-8",
    ) as f:
        analysis = json.load(f)

    summary = analysis["scenarios"]

    low_v = summary["low"]["maximum_V"]["value"]
    medium_v = summary["medium"]["maximum_V"]["value"]
    high_v = summary["high"]["maximum_V"]["value"]

    low_dvdt = summary["low"]["maximum_dVdt"]["value"]
    medium_dvdt = summary["medium"]["maximum_dVdt"]["value"]
    high_dvdt = summary["high"]["maximum_dVdt"]["value"]

    checks["V_monotonic_with_severity"] = check(
        high_v > medium_v > low_v
    )

    checks["dVdt_monotonic_with_severity"] = check(
        high_dvdt > medium_dvdt > low_dvdt
    )

    checks["low_max_V"] = check(
        abs(low_v - 200.5) < 1e-9
    )

    checks["medium_max_V"] = check(
        abs(medium_v - 800.5) < 1e-9
    )

    checks["high_max_V"] = check(
        abs(high_v - 2450.5) < 1e-9
    )

    checks["low_max_dVdt"] = check(
        abs(low_dvdt - 15000.0) < 1e-6
    )

    checks["medium_max_dVdt"] = check(
        abs(medium_dvdt - 75000.0) < 1e-6
    )

    checks["high_max_dVdt"] = check(
        abs(high_dvdt - 240000.0) < 1e-6
    )

    validation_passed = all(checks.values())

    result = {
        "experiment": "EXP-008",
        "description": (
            "Consistency validation of EXP-006 "
            "and EXP-007 sensitivity results"
        ),
        "checks": checks,
        "validation_passed": validation_passed,
    }

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
